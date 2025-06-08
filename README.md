# Filename2EXIFDate
* execute the tool from cli
  ```python -m filename2exifdate.filename2exifdate -dir ../tests/samples```
  
## ToDos
* [ ] Cleanup Repo and Readme
* [ ] Renaming of package
* [ ] Check that CLI works
* [ ] Add Progressbar (tqdm)
* [ ] Multithreading of recursive task
* [ ] add Testcases (add some images to test the code)
* [ ] package optional

## Links used
* logging: https://www.machinelearningplus.com/python/python-logging-guide/
* cli: https://www.geeksforgeeks.org/§command-line-scripts-python-packaging/?ref=header_search
* package pypi: pypi conform repo https://packaging.python.org/en/latest/tutorials/packaging-projects/, https://pybit.es/articles/how-to-package-and-deploy-cli-apps/, https://setuptools.pypa.io/en/latest/userguide/entry_point.html

## Logs
* Windows ...
* Linux ...
* Custom ...


## Prequisite
...

## Build
1. create a virtual environment: ```python -m venv venv```
2. activate the virtual environment: ```source ./venv/bin/activate```
3. install the development dependencies: ```pip install -m requirements.txt```
4. build the package: ```python -m build```
5. install package in editable mode: ```pip install -e .```