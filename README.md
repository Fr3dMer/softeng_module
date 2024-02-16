PanelAppDB
============

PanelAppDB is a tool to search and store gene panel information for genetic tests included in the National Genomic Testing Directory.

- For help please use `-h` command

Functionality
---------------
Functionality provided by PanelAppDB include:
- Search for gene panel information by R code
- Generate BED file for gene panels
- Search for gene panels used for specific patients

ReadTheDocs documentation available at: https://softeng-module-amyg.readthedocs.io/en/latest/

Installation
---------------

# Install via conda
```bash
# Clone PanelAppDB from Github repository
git clone https://github.com/Fr3dMer/softeng_module.git
# Create conda environment
conda env create -n PanelAppDB --file environment.yml
# Activate conda environment
conda activate PanelAppDB
# Create directory to house your database
mkdir db
```

# Install via pip 
```bash
# Clone PanelAppDB from Github repository
git clone https://github.com/Fr3dMer/softeng_module.git
# Install requirements
# Recommend creating venv or conda environment and activating it before carrying out this step
pip install -r docs/requirements.txt
# Create directory to house your database
mkdir db
```

Usage
------
PanelAppDB can be run in the conda environent created in the steps above, or in a Docker container.

# Running script localy using conda environment
To run in the conda enviroment, ensure the environment is activated and submit your desired query using the corresponding arguments (discussed below).
eg:
```bash
conda activate PanelAppDB
python PanelAppDB.py <PARAMS HERE>
# Example:
python PanelAppDB.py -r R45
```

# Building and running script inside container 
To run in a container, build the container in docker then run it with docker run.
eg:
```bash
sudo docker build --rm -t "panel_app_db" .
sudo docker run --rm panel_app_db <PARAMS HERE>
# example:
sudo docker run --rm panel_app_db -r R45 
```

# Retreiving Pannel Information
Once the tool is successfully installed, it can be used to retrieve panel information.

Search by r-code:
```bash
# To search by r-code, use the -r or --rcode flag
python PanelAppDB.py -r R45
```



Tests
---------------
To run tests, run the following command in root:
```bash
pytest test/
```


## Structure of app
![flow chart showing structure of app](docs/Flowchart.png)


## Licence
### MIT Licence
Copyright 2024 Fredrick, Abi, Amy

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.


THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

