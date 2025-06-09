import os
from PIL import Image
import piexif

SAMPLES_DIR = os.path.join(os.path.dirname(__file__), "samples")
os.makedirs(SAMPLES_DIR, exist_ok=True)


def create_image(path, color=(255, 0, 0)):
    img = Image.new("RGB", (100, 100), color)
    img.save(path, "JPEG")


def set_exif_date(path, date_str):
    exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
    exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = date_str
    exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized] = date_str
    exif_bytes = piexif.dump(exif_dict)
    img = Image.open(path)
    img.save(path, exif=exif_bytes)


# 1. Bild mit passendem Dateinamen und EXIF-Datum
img1 = os.path.join(SAMPLES_DIR, "IMG_20220101_120000.jpg")
create_image(img1)
set_exif_date(img1, "2022:01:01 12:00:00")

# 2. Bild mit passendem Dateinamen, aber ohne EXIF-Datum
img2 = os.path.join(SAMPLES_DIR, "IMG_20220102_130000.jpg")
create_image(img2)
# Kein EXIF gesetzt

# 3. Bild mit passendem Dateinamen, aber falschem EXIF-Datum
img3 = os.path.join(SAMPLES_DIR, "IMG_20220103_140000.jpg")
create_image(img3)
set_exif_date(img3, "2020:01:01 00:00:00")

# 4. Bild mit ungültigem Dateinamen, aber EXIF-Datum
img4 = os.path.join(SAMPLES_DIR, "randomfile.jpg")
create_image(img4)
set_exif_date(img4, "2022:05:05 15:30:00")

# 5. PNG-Bild ohne EXIF
img5 = os.path.join(SAMPLES_DIR, "IMG_20220104_150000.png")
img = Image.new("RGB", (100, 100), (0, 255, 0))
img.save(img5, "PNG")

print("Testbilder wurden in 'tests/samples' erzeugt.")
