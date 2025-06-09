# exifdatefix

**exifdatefix** is a command-line tool for checking and correcting EXIF date metadata in image files. \
It scans directories for images, compares the dates in filenames with the embedded EXIF dates, and can update the EXIF data to match the filename if needed.  
This is useful for organizing and fixing photo collections where file dates and metadata are inconsistent, such as after copying from different devices or recovering files.

## Usage Examples
* Execute CLI, in dry-mode to check with the logs what the force mode would change
  ```python -m exifdatefix.cli -dir ~/Bilder/```
  
* Execute CLI, in force-mode applies changes
  ```python -m exifdatefix.cli -f -dir ~/Bilder/```
  
## Development Instructions
### Build
1. create a virtual environment: ```python -m venv venv```
2. activate the virtual environment: ```source ./venv/bin/activate```
3. install the development dependencies: ```pip install -r requirements-dev.txt```
4. build the package: ```python -m build```
5. install package in editable mode: ```pip install -e .```

### Test
1. open project folder in bash: ```cd exifdatefix```
2. run: ```pytest -v```
   
## Todo
* [ ] Improve test cases:
  - Increase test coverage to include untested functions and modules.
  - Add edge case scenarios (e.g., invalid inputs, large datasets).
  - Optimize performance testing for recursive tasks.
* [ ] Add CLI option for log directory in the CLI script (e.g., `cli.py`):
  ```python
  parser.add_argument("--log-dir", default=LOG_DIRECTORY, help="Path to log file")
  ```
* [ ] optimize speed of recursive task (for multiple folders) e.g. multithreading
* [ ] package to pypi (Follow this guide to publish: https://packaging.python.org/en/latest/tutorials/packaging-projects/)

## Helpful Links
* package pypi:
  * [pypi conform repo](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
  * [How to package and deploy CLI apps](https://pybit.es/articles/how-to-package-and-deploy-cli-apps/)
  * [Setuptools entry points](https://setuptools.pypa.io/en/latest/userguide/entry_point.html)
* logging: https://www.machinelearningplus.com/python/python-logging-guide/
* cli: https://www.geeksforgeeks.org/command-line-scripts-python-packaging/?ref=header_search
