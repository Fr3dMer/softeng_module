# syntax=docker/dockerfile:1

FROM continuumio/miniconda3
WORKDIR /app
COPY . .

ENV panelid 3
ENV rcode default_env_value


RUN conda env create --name pannelappdb --file environment.yml

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "pannelappdb","python3","PannelAppDB.py"]

 