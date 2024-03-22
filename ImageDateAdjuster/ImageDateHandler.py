import json
import toml
import os
from time import time
from datetime import datetime
import logging
import dateutil.parser as parser
from exiftool import ExifToolHelper


def setup_logging():
    log_directory = "logs"
    os.makedirs(log_directory, exist_ok=True)
    log_filename = f"logfile_{datetime.now().strftime('%y%m%d')}.log"
    log_filepath = os.path.join(log_directory, log_filename)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler(log_filepath)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def load_config():
    try:
        return toml.load("pyproject.toml")["application"]
    except (FileNotFoundError, KeyError) as e:
        logger.warning(f"Failed to load configuration: {e}")
        return {
            "allowed_time_deviation": 5,
            "additional_formats": [],
        }  # Provide default config values


logger = setup_logging()
APP_CONFIG = load_config()


def timer(func):
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        logger.debug(f"Function {func.__name__!r} executed in {(t2-t1):.4f}s")
        return result

    return wrap_func


def get_all_subdirectories(dirname: str, visited: set[str] = None) -> list[str]:
    if visited is None:
        visited = set()
        subdirectories = [dirname]
    else:
        subdirectories = []

    with os.scandir(dirname) as entries:
        for entry in entries:
            if entry.is_dir() and entry.path not in visited:
                visited.add(entry.path)
                subdirectories.append(entry.path)
                subdirectories.extend(get_all_subdirectories(entry.path, visited))

    return subdirectories


class ImageDateHandler:
    def __init__(
        self,
        dirname: str,
        dryrun: bool = True,
        max_timedeviation_sec: int = 60,
        filetypes: tuple[str, ...] = ("jpg"),
        additional_formats: tuple[str, ...] = (),
    ):
        self.dirname = dirname
        self.filetypes = filetypes
        self.dryrun = dryrun
        self.timetolerance_sec = max_timedeviation_sec
        self.additional_formats = additional_formats
        self.imagefiles = []
        self.filepaths = []
        self.filenamedates = []
        self.exifdates = []
        self.has_timedifference = []

        logger.info(f"Current directory: {self.dirname}")
        logger.info(f"Execution in Dry-Run Mode: {self.dryrun}")
        self.extract_image_files()
        self.extract_filename_dates()
        self._update_filepaths()
        self.extract_exif_dates()

    def get_image_files(self):
        return self.imagefiles

    def get_filename_dates(self):
        return self.filenamedates

    def get_exif_dates(self):
        return self.exifdates

    def extract_image_files(self):
        self.imagefiles = list(
            filter(
                lambda x: x.lower().endswith(self.filetypes), os.listdir(self.dirname)
            )
        )
        logger.info(f"{len(self.imagefiles)} image files {self.filetypes} found!")
        logger.debug(f"Filenames: {self.imagefiles}")

    def extract_filename_dates(self):
        for datestring in self.imagefiles:
            date = None
            try:
                date = parser.parse(datestring, fuzzy_with_tokens=False, fuzzy=False)
            except ValueError:
                for date_format in self.additional_formats:
                    try:
                        date = datetime.strptime(datestring, date_format)
                    except ValueError:
                        continue  # If current format doesn't match, try next
                    else:
                        break
            finally:
                self.filenamedates.append(date)

            if date is None:
                logger.info(f"Couldn't parse:{datestring}")

        logger.debug(f"Filenamedates: {self.filenamedates}")

    def extract_exif_dates(self):
        if self.filepaths:
            with ExifToolHelper() as et:
                taglist = et.get_tags(self.filepaths, tags=["CreateDate"])

            for element in taglist:
                datestring = element.get("EXIF:CreateDate")
                if datestring is not None:
                    createdate = datetime.strptime(datestring, "%Y:%m:%d %H:%M:%S")
                else:
                    createdate = None

                self.exifdates.append(createdate)

            logger.debug(f"Exifdates: {self.exifdates}")

    def compare_dates(self):
        for exifdate, filedate in zip(self.exifdates, self.filenamedates):
            if exifdate is not None and filedate is not None:
                delta = abs((exifdate - filedate))
                self.has_timedifference.append(delta.seconds > self.timetolerance_sec)
            elif filedate is None:
                self.has_timedifference.append(False)
            else:
                self.has_timedifference.append(True)
        logger.debug(f"Has Timedifference: {self.has_timedifference}")

    def update_exif_dates(self):
        changes = {}
        with ExifToolHelper() as et:
            for file_path, creation_date, exifdate, has_delta in zip(
                self.filepaths,
                self.filenamedates,
                self.exifdates,
                self.has_timedifference,
            ):
                if has_delta:
                    new_create_date = creation_date.strftime("%Y:%m:%d %H:%M:%S")
                    command = {
                        "-DateTimeOriginal=" + new_create_date,
                        "-CreateDate=" + new_create_date,
                        "-overwrite_original",
                        file_path,
                    }
                    try:
                        if self.dryrun:
                            pass
                        else:
                            et.execute(*command)
                    except Exception as e:
                        logger.error(f"Error ExifToolHelper: {e}")

                    logger.info(
                        f"File: {file_path}, changed 'CreationDate'"
                        f"to: {new_create_date}"
                    )

                    changes[file_path] = {
                        "new_creation_date": str(creation_date),
                        "old_creation_date": str(exifdate),
                    }
        return changes

    def _update_filepaths(self):
        self.filepaths = [
            os.path.join(self.dirname, filename) for filename in self.imagefiles
        ]


def app():
    subdirectories = get_all_subdirectories("data/test")
    logfilename = datetime.now().strftime("%y%m%d_%H%M%S_") + "logfile"
    changes = {}
    max_subdirectories = len(subdirectories)
    for item, directory in enumerate(subdirectories, start=1):
        print(f"Directory {item} of {max_subdirectories}")
        directorypath = os.path.normpath(directory)
        ida = ImageDateHandler(
            dirname=directorypath,
            dryrun=True,
            max_timedeviation_sec=APP_CONFIG["allowed_time_deviation"],
            filetypes=("jpg", "png"),
            additional_formats=APP_CONFIG["additional_formats"],
        )
        ida.compare_dates()
        result = ida.update_exif_dates()
        changes.update(result)

    with open("logs/" + logfilename + ".json", "w") as outfile:
        json.dump(changes, outfile, indent=4)


if __name__ == "__main__":
    app()
