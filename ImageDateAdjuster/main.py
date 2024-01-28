import toml
import os
import ImageDateHandler as idh

APP_CONFIG = toml.load("pyproject.toml")["app"]


def app():
    print(APP_CONFIG["default_directory"])
    myList = idh.get_all_subdirectories(APP_CONFIG["default_directory"])
    for directory in myList:
        print("-*-*-*-*-")
        myPath = os.path.normpath(directory)
        print(myPath)
        myida = idh.ImageDateHandler(myPath, APP_CONFIG["allowed_time_deviation"])
        print(myida.get_image_files())
        print(myida.get_filename_dates())
        print(myida.get_exif_dates())
        print(myida.compare_dates())
        print(myida.update_exif_dates())


if __name__ == "__main__":
    app()
