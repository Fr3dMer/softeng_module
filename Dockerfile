# syntax=docker/dockerfile:1

FROM continuumio/miniconda3
WORKDIR /app
COPY . .


RUN conda env create --name pannelappdb --file environment.yml

CMD ["conda", "run", "--no-capture-output", "-n", "pannelappdb","python3","PannelAppDB.py","-p 3"] 