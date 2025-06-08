import logging
import json
import os
import argparse
from tqdm import tqdm
from datetime import datetime
from .core import ImageDateHandler

LOG_DIRECTORY = os.path.join(os.path.expanduser("~"), "logs")

log_file_name = f"{datetime.now().strftime('%y%m%d')}_exifdatefix_log.log"
log_file_path = os.path.join(LOG_DIRECTORY, log_file_name)

if not os.path.exists(LOG_DIRECTORY):
    os.makedirs(LOG_DIRECTORY)

logging.basicConfig(
    filemode="a",  # Change "w" to "a" to append instead of overwrite
    filename=log_file_path,
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

changelog_file_name = (
    f"{datetime.now().strftime('%y%m%d_%H%M%S')}_exifdatefix_changelog.json"
)
changelog_file_path = os.path.join(LOG_DIRECTORY, changelog_file_name)


def filenames_to_exif_dates(root_directory, force=False):
    sub_directories = ImageDateHandler.get_all_subdirectories(root_directory)
    exif_date_changes = {}
    max_subdirectories = len(sub_directories)
    with tqdm(
        total=max_subdirectories,
        desc="Processing directories",
        unit="dir",
        leave=True,
    ) as pbar:
        for item, directory in enumerate(sub_directories, start=1):
            directory_path = os.path.normpath(directory)
            ida = ImageDateHandler(
                dirname=directory_path,
                force=force,
            )
            ida.compare_dates()
            result = ida.update_exif_dates()
            exif_date_changes.update(result)
            pbar.update(1)

    with open(changelog_file_path, "w") as outfile:
        json.dump(exif_date_changes, outfile, indent=4)


def main():
    # create parser object
    parser = argparse.ArgumentParser(
        prog="exifdatefix", description="A tool to check an correct EXIF Dates!"
    )

    # defining arguments for parser object
    parser.add_argument(
        "-dir",
        type=str,
        nargs=1,
        metavar="dir",
        help="The directory to process exifdatefix, default current directory",
    )

    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="To write the exif dates, force needs to be set",
    )

    # parse the arguments from standard input
    args = parser.parse_args()

    if args.dir is None:
        directory = os.getcwd()
    else:
        directory = args.dir[0]

    forcemode = args.force

    print(f'"exifdatefix" executes in {directory} with force-mode={forcemode}')
    filenames_to_exif_dates(directory, forcemode)

    print(f"Execution logs: {LOG_DIRECTORY}")


if __name__ == "__main__":
    main()
