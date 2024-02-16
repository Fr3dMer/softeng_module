# Dockerfile for building containers for this app

# Get latest ubuntu LTS release
FROM ubuntu:latest
WORKDIR /app
COPY . .

# Update package index and instal pip
RUN apt-get update && apt-get install -y \
    python3-pip

# Install requirements found in requirements.txt using pip
RUN pip install -r docs/requirements.txt

# Entry to script
ENTRYPOINT ["python3","-W ignore::DeprecationWarning","panel_app_db.py"]