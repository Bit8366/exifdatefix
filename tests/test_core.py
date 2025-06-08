import os
import tempfile
import shutil
from datetime import datetime
import pytest
from exifdatefix.core import ImageDateHandler


@pytest.fixture
def temp_image_dir():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


def create_image_file(directory, filename):
    path = os.path.join(directory, filename)
    with open(path, "wb") as f:
        f.write(b"fake image data")
    return path


def test_extract_image_files_jpg_and_png(temp_image_dir):
    create_image_file(temp_image_dir, "IMG_20220101_120000.jpg")
    create_image_file(temp_image_dir, "IMG_20220101_120000.png")
    create_image_file(temp_image_dir, "not_an_image.txt")
    handler = ImageDateHandler(temp_image_dir)
    assert sorted(handler.get_image_files()) == sorted(
        ["IMG_20220101_120000.jpg", "IMG_20220101_120000.png"]
    )


def test_extract_filename_dates_valid_and_invalid(temp_image_dir):
    create_image_file(temp_image_dir, "IMG_20220101_120000.jpg")
    create_image_file(temp_image_dir, "invalidname.jpg")
    handler = ImageDateHandler(temp_image_dir)
    dates = handler.get_filename_dates()
    assert isinstance(dates[0], datetime)
    assert dates[1] is None


def test_extract_exif_dates(temp_image_dir):
    create_image_file(temp_image_dir, "IMG_20220101_120000.jpg")
    handler = ImageDateHandler(temp_image_dir)
    # Simulate EXIF date extraction
    handler.exif_dates = [datetime(2022, 1, 1, 12, 0, 0)]
    assert handler.get_exif_dates() == [datetime(2022, 1, 1, 12, 0, 0)]


def test_get_all_subdirectories(tmp_path):
    sub1 = tmp_path / "sub1"
    sub2 = tmp_path / "sub2"
    sub1.mkdir()
    sub2.mkdir()
    sub1a = sub1 / "sub1a"
    sub1a.mkdir()
    result = ImageDateHandler.get_all_subdirectories(str(tmp_path))
    assert str(tmp_path) in result
    assert str(sub1) in result
    assert str(sub2) in result
    assert str(sub1a) in result


def test_compare_dates_sets_has_time_difference(temp_image_dir):
    create_image_file(temp_image_dir, "IMG_20220101_120000.jpg")
    handler = ImageDateHandler(temp_image_dir)
    # Simulate exif_dates and filename_dates
    handler.exif_dates = [datetime(2022, 1, 1, 12, 0, 0)]
    handler.filename_dates = [datetime(2022, 1, 1, 12, 2, 1)]
    handler.compare_dates()
    assert handler.has_time_difference == [True]


def test_compare_dates_handles_none(temp_image_dir):
    create_image_file(temp_image_dir, "IMG_20220101_120000.jpg")
    handler = ImageDateHandler(temp_image_dir)
    handler.exif_dates = [None]
    handler.filename_dates = [datetime(2022, 1, 1, 12, 0, 0)]
    handler.compare_dates()
    assert handler.has_time_difference == [True]


def test_compare_dates_handles_filedate_none(temp_image_dir):
    create_image_file(temp_image_dir, "IMG_20220101_120000.jpg")
    handler = ImageDateHandler(temp_image_dir)
    handler.exif_dates = [datetime(2022, 1, 1, 12, 0, 0)]
    handler.filename_dates = [None]
    handler.compare_dates()
    assert handler.has_time_difference == [False]
