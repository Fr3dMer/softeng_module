# A fully rendered markdown file (README.md) that describes the project

# PannelAppDB

## Install 
```bash
git clone https://github.com/Fr3dMer/softeng_module.git
conda env create -n PannelAppDB --file environment.yml
conda activate PannelAppDB
```

## Building and running script inside container 
```bash
sudo docker build -t "panel_app_db" .
sudo docker logs -f $(sudo docker run -d panel_app_db <PARAMS HERE>)
```


## Running script 
```bash


```

## Tests
```bash


```



## Proposed structure of app
![flow chart showing structure of app](docs/Flowchart.png)

