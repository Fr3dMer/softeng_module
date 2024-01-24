# syntax=docker/dockerfile:1


FROM continuumio/miniconda3
WORKDIR /app
COPY . .

# Create conda env, init and activate. BUT do not use conda to install any libs, 
# this will be done by pip
RUN conda env create --name pannelappdb 


# Update package index and instal pip
RUN apt-get update && apt-get install -y \
    python3-pip

# Install requirements found in requirements.txt using pip in conda env
RUN pip install -r docs/requirements.txt

# Entry to script

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "pannelappdb","python3","PannelAppDB.py"]