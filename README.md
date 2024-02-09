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



## Install 
```bash
git clone https://github.com/Fr3dMer/softeng_module.git
cd softeng_module
conda env create -n PanelAppDB --file environment.yml
conda activate PanelAppDB
```

## Building and running script inside container 
```bash
sudo docker build -t "panel_app_db" .
sudo docker logs -f $(sudo docker run -d panel_app_db <PARAMS HERE>)
# example
sudo docker logs -f $(sudo docker run -d panel_app_db -p 3)
```


## Running script localy 
```bash
conda activate PannelAppDB
python3 PannelAppDB.py -r R45
```

## Tests
```bash
pytest test/
```



## Proposed structure of app
![flow chart showing structure of app](docs/Flowchart.png)

