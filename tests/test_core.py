import os
from datetime import datetime
from exifdatefix.core import ImageDateHandler

SAMPLES_DIR = os.path.join(os.path.dirname(__file__), "samples")


def test_extract_image_files_jpg_and_png():
    handler = ImageDateHandler(SAMPLES_DIR)
    files = handler.get_image_files()
    expected_files = [
        "IMG_20220101_120000.jpg",
        "IMG_20220102_130000.jpg",
        "IMG_20220103_140000.jpg",
        "IMG_20220104_150000.png",
        "randomfile.jpg",
    ]
    assert sorted(files) == sorted(expected_files)


def test_extract_exif_dates():
    handler = ImageDateHandler(SAMPLES_DIR)
    exif_dates = handler.get_exif_dates()
    expected_dates = [
        datetime(2022, 1, 1, 12, 0, 0),
        None,  # Kein EXIF-Datum für IMG_20220102_130000.jpg
        datetime(
            2020, 1, 1, 0, 0, 0
        ),  # Falsches EXIF-Datum für IMG_20220103_140000.jpg
        datetime(2022, 5, 5, 15, 30, 0),  # EXIF-Datum für randomfile.jpg
        None,  # Kein EXIF-Datum für PNG-Bild
    ]
    assert sorted(exif_dates, key=lambda x: (x is not None, x)) == sorted(
        expected_dates, key=lambda x: (x is not None, x)
    )
