# Filename2EXIFDate
* here some content

## ToDos
* [x] logging https://www.machinelearningplus.com/python/python-logging-guide/
* [x] exceptio file formats to config!
* [x] toml file basics https://toml.io/en/
* [x] Threema Dateformat Problem (e.g. config file?? for unknown formats)
* [x] Error Handling: TryExcept, ask for prompt, log, etc. (make file write protected to check)
* [x] Silent and Manual mode 
* [x] command line arguments https://www.geeksforgeeks.org/§command-line-scripts-python-packaging/?ref=header_search
* [x] cleanup naming (EXIFDateCorrector)
* [x] define log directory default /var/logs/filename2exif... and windows %APPDATA%/filename2.. ....
* [ ] make setup.py etc and pypi conform repo https://packaging.python.org/en/latest/tutorials/packaging-projects/, https://pybit.es/articles/how-to-package-and-deploy-cli-apps/, https://setuptools.pypa.io/en/latest/userguide/entry_point.html
* [ ] add description and manual to readme
* [ ] test in linux and windows
* [ ] test images in repo data
* [ ] testcases implementation
* [ ] additional formats better place
* [ ] log directory as cli parameter

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