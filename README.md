# exifdatefix

## Usage
* Execute CLI, in dry-mode to check with the logs what the force mode would change
  ```python -m exifdatefix.cli -dir ~/Bilder/```
  
* Execute CLI, in force-mode applies changes
  ```python -m exifdatefix.cli -f -dir ~/Bilder/```
  
## Development
### Build
1. create a virtual environment: ```python -m venv venv```
2. activate the virtual environment: ```source ./venv/bin/activate```
3. install the development dependencies: ```pip install -m requirements-dev.txt```
4. build the package: ```python -m build```
5. install package in editable mode: ```pip install -e .```

### Test
1. open project folder in bash: ```cd exifdatefix```
2. run: ```pytest -v```
   
## Todo
* [x] Cleanup Repo and Readme
* [x] Renaming of package
* [x] Check that CLI works
* [ ] add CLI to chang log-directory ```parser.add_argument("--log-dir", default=LOG_DIRECTORY, help="Path to log file")```
* [x] Add Progressbar (tqdm)
* [ ] Multithreading of recursive task
* [x] add Testcases (add some images to test the code)
* [ ] package to pypi
* [ ] make better testcases

## Helpful Links
* logging: https://www.machinelearningplus.com/python/python-logging-guide/
* cli: https://www.geeksforgeeks.org/§command-line-scripts-python-packaging/?ref=header_search
* package pypi: pypi conform repo https://packaging.python.org/en/latest/tutorials/packaging-projects/, https://pybit.es/articles/how-to-package-and-deploy-cli-apps/, https://setuptools.pypa.io/en/latest/userguide/entry_point.html