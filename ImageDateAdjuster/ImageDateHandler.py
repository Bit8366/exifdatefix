import os
from time import time
from datetime import datetime

import dateutil.parser as parser
from exiftool import ExifToolHelper


def timer(func):
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f"Function {func.__name__!r} executed in {(t2-t1):.4f}s")
        return result

    return wrap_func


def get_all_subdirectories(dirname: str, visited: set[str] = None) -> list[str]:
    if visited is None:
        visited = set()

    subdirectories = [dirname]
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
        dirname: os.path,
        max_timedeviation_sec: int = 60,
        filetypes: tuple[str, ...] = ("jpg"),
    ):
        self.dirname = dirname
        self.filetypes = filetypes
        self.timetolerance_sec = max_timedeviation_sec
        self.imagefiles = []
        self.filepaths = []
        self.filenamedates = []
        self.exifdates = []
        self.has_timedifference = []

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
            filter(lambda x: x.endswith(self.filetypes), os.listdir(self.dirname))
        )

    def extract_filename_dates(self):
        for datestring in self.imagefiles:
            try:
                date = parser.parse(datestring, fuzzy_with_tokens=False, fuzzy=True)
                self.filenamedates.append(date)
            except ValueError as e:
                print(f"Error parsing '{datestring}': {e}")

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
        return self.exifdates

    def compare_dates(self):
        for date1, date2 in zip(self.exifdates, self.filenamedates):
            if date1 is not None and date2 is not None:
                delta = abs((date1 - date2).seconds)
                self.has_timedifference.append(delta > self.timetolerance_sec)
            else:
                self.has_timedifference.append(True)
        return self.has_timedifference

    def update_exif_dates(self):
        file_paths = [
            item
            for item, condition in zip(self.filepaths, self.has_timedifference)
            if condition
        ]
        creation_dates = [
            item
            for item, condition in zip(self.filenamedates, self.has_timedifference)
            if condition
        ]
        with ExifToolHelper() as et:
            for file_path, creation_date in zip(file_paths, creation_dates):
                exif_create_date = creation_date.strftime("%Y:%m:%d %H:%M:%S")
                command = {
                    "-DateTimeOriginal=" + exif_create_date,
                    "-CreateDate=" + exif_create_date,
                    "-overwrite_original",
                    file_path,
                }
                et.execute(*command)

    def _update_filepaths(self):
        self.filepaths = [
            os.path.join(self.dirname, filename) for filename in self.imagefiles
        ]
