import os
from datetime import datetime
import logging
import dateutil.parser as parser
from exiftool import ExifToolHelper

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

DATETIME_PARSE_FORMATS = [
    "threema-%Y%m%d-%H%M%S%f.jpg",
    "IMG-%Y%m%d-WA%f.jpg",
    "%Y%m%d_%H%M%S.jpg",
    "%Y%m%d_%H%M%S(%f).jpg",
    "IMG_%Y%m%d_%H%M%S.jpg",
    "VideoCapture_%Y%m%d-%H%M%S.jpg",
    "image-%Y%d%m-%H%M%S.jpg",
    "image-%Y%d%m-%H%M%S (%f).jpg",
    # Add more formats as needed
]
MAX_TIME_DEVIATION_SECONDS = 120
FILE_TYPES = ("jpg", "png")


class ImageDateHandler:
    def __init__(
        self,
        dirname: str,
        force: bool = False,
        max_time_deviation_sec: int = MAX_TIME_DEVIATION_SECONDS,
        file_types: tuple[str, ...] = FILE_TYPES,
        datetime_parse_formats: tuple[str, ...] = DATETIME_PARSE_FORMATS,
    ):
        self.dirname = dirname
        self.file_types = file_types
        self.force = force
        self.max_time_deviation_sec = max_time_deviation_sec
        self.datetime_parse_formats = datetime_parse_formats
        self.image_files = []
        self.filepaths = []
        self.filename_dates = []
        self.exif_dates = []
        self.has_time_difference = []

        logger.info(f"Current directory: {self.dirname}")
        logger.info(f"Execution in Force Mode: {self.force}")
        self.extract_image_files()
        self.extract_filename_dates()
        self._update_filepaths()
        self.extract_exif_dates()

    def get_image_files(self):
        return self.image_files

    def get_filename_dates(self):
        return self.filename_dates

    def get_exif_dates(self):
        return self.exif_dates

    def extract_image_files(self):
        self.image_files = list(
            filter(
                lambda x: x.lower().endswith(self.file_types), os.listdir(self.dirname)
            )
        )
        logger.info(f"{len(self.image_files)} image files {self.file_types} found!")
        logger.debug(f"Filenames: {self.image_files}")

    def extract_filename_dates(self):
        for datestring in self.image_files:
            date = None
            try:
                date = parser.parse(datestring, fuzzy_with_tokens=False, fuzzy=False)
            except ValueError:
                for date_format in self.datetime_parse_formats:
                    try:
                        date = datetime.strptime(datestring, date_format)
                    except ValueError:
                        continue  # If current format doesn't match, try next
                    else:
                        break
            finally:
                self.filename_dates.append(date)

            if date is None:
                logger.info(f"Couldn't parse:{datestring}")

        logger.debug(f"Filenamedates: {self.filename_dates}")

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

                self.exif_dates.append(createdate)

            logger.debug(f"Exifdates: {self.exif_dates}")

    def compare_dates(self):
        for exifdate, filedate in zip(self.exif_dates, self.filename_dates):
            if exifdate is not None and filedate is not None:
                delta = abs((exifdate - filedate))
                self.has_time_difference.append(
                    delta.seconds > self.max_time_deviation_sec
                )
            elif filedate is None:
                self.has_time_difference.append(False)
            else:
                self.has_time_difference.append(True)
        logger.debug(f"Has Timedifference: {self.has_time_difference}")

    def update_exif_dates(self):
        changes = {}
        with ExifToolHelper() as et:
            for file_path, creation_date, exifdate, has_delta in zip(
                self.filepaths,
                self.filename_dates,
                self.exif_dates,
                self.has_time_difference,
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
                        if self.force:
                            et.execute(*command)
                        else:
                            pass
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
            os.path.join(self.dirname, filename) for filename in self.image_files
        ]

    @staticmethod
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
                    subdirectories.extend(
                        ImageDateHandler.get_all_subdirectories(entry.path, visited)
                    )

        return subdirectories
