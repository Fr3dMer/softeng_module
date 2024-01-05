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
sudo docker build -t "test" . 
sudo docker run --name=myapp -e PYTHONUNBUFFERED=1 -d test
# to see stdout
sudo docker logs myapp 
```


## Running script 
```bash


```

## Tests
```bash


```



## Proposed structure of app
![flow chart showing structure of app](docs/Flowchart.png)

