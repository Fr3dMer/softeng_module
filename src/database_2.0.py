# script created using the following websites:
# https://www.datacamp.com/tutorial/sqlalchemy-tutorial-examples
# https://towardsdatascience.com/sqlalchemy-python-tutorial-79a577141a91
# https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#declaring-simple-constraints

import sqlalchemy as db
from sqlalchemy import MetaData, Table, Column, String, Date, Float, LargeBinary, ForeignKey, text, and_, or_
from sqlalchemy.sql import select

import pandas as pd
import datetime
import json

# imports the SQLAlchemy library and renames it as "db"
# imports required objects from sqlalchemy

engine = db.create_engine('sqlite:///panel_app_db.db')
# Creates a database engine using the SQLite dialect and specifies the name of the database file
# Engine is stored in the "engine" variable

connection = engine.connect()
# Connection to the database established using the "connect()" method of the engine.
# This is stored in the "connection" variable

metadata = MetaData()
# Extracting the metadata
# This line creates a MetaData object which is used to store information about the database schema

samples = db.Table('samples', metadata,
                   db.Column('sample_id', db.String(255), primary_key=True, nullable=False),
                   db.Column('patient_id', db.String(255), nullable=False),
                   db.Column('unique_panel_id', db.String(255), ForeignKey('panels.unique_panel_id'), nullable=False),
                   db.Column('date', db.Date())
                   )
# Creates the table object named samples
# Metadata creates a new meta data objet which holds information about the table
# The Column() function is used to create each column, with the first argument being the name of the columm and the second argument being the data type

panels = db.Table('panels', metadata,
                  db.Column('unique_panel_id', db.String(255), primary_key=True, nullable=False),
                  db.Column('r_code', db.String(255), nullable=False),
                  db.Column('version', db.Float(), nullable=False),
                  db.Column('gene_details', db.String(255), nullable=False),
                  db.Column('JSON', LargeBinary),
                  db.Column('BED_file_GrCH37', String),
                  db.Column('BED_file_GrCH38', String),
                  )

# Creates the table object named panels
# Metadata creates a new meta data objet which holds information about the table
# The Column() function is used to create each column, with the first argument being the name of the columm and the second argument being the data type

metadata.create_all(engine)
# metadata.drop_all(engine)
# Here, the create_all method of the metadata object is called with the engine object as an argument
# This creates the tables in the database

#print("Columns in 'samples' table:", samples.columns.keys())
#print("Columns in 'panels' table:", panels.columns.keys())
# Print information about the 'samples' table columns

###################################################################################################
###################################################################################################

# Inserting records into tables
query = db.insert(samples).values(sample_id='EX100', patient_id='PID10', unique_panel_id='R111-1.1',
                                  date=datetime.date(2023, 12, 10))
record = connection.execute(query)

query = db.insert(samples).values(sample_id='EX122', patient_id='PID15', unique_panel_id='R111-1.2',
                                  date=datetime.date(2024, 1, 18))
record = connection.execute(query)

# Loading API.json file to test DB
def load_json_file(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        return data

# path to JSON file
file_path = 'API_test.json'

# variable for storing json file
json_file = load_json_file(file_path)
# Convert JSON data to bytes
json_data_bytes = json.dumps(json_file).encode('utf-8')

query = db.insert(panels).values(
    unique_panel_id='R111-1.1',
    r_code='R111',
    version=1.1,
    gene_details='MTHFR, HGNC;7436, 1:11845780-11866977, 1:11785723-11806920',
    JSON=json_data_bytes,
    BED_file_GrCH37='',
    BED_file_GrCH38='')
record = connection.execute(query)

query = db.insert(panels).values(
    unique_panel_id='R111-1.2',
    r_code='R111',
    version=1.2,
    gene_details='MTHFR, DHFR, HGNC;7436, 1:11845780-11866977, 1:11785723-11806920',
    JSON=json_data_bytes,
    BED_file_GrCH37='',
    BED_file_GrCH38='')
record = connection.execute(query)

# Use the table object to run the query and extract the results
# The query is executed using a database connection object called connection
# using the select method, to select all columns in the samples table - use the columns
# attribute of the table to get the columns and pass that to the select function
# the results of the query are stored in the output variable

###################################################################################################################
###################################################################################################################

#Function for inserting a new version of a GMS panel
def insert_new_panel(unique_panel_id, r_code, version, gene_details, JSON, BED_file_GrCH37, BED_file_GrCH38):

# check this panel isn't already in db (could put into seperate function)
    list_of_unique_id_and_version = connection.execute(db.select(panels.columns.version)\
    .where(panels.columns.r_code == r_code)).fetchall()

# Code to check version is not already present
    if version not in list_of_unique_id_and_version:
        query = connection.execute(db.insert(panels).values(
        unique_panel_id=unique_panel_id,
        r_code=r_code,
        version=version,
        gene_details= gene_details,
        JSON=JSON,
        BED_file_GrCH37=BED_file_GrCH37,
        BED_file_GrCH38=BED_file_GrCH38))

#return a boolean indicating whether the operation was successful
        return True

    else:
        print("Panel with the same r_code and version already exists")
        return False

new_panel_input = insert_new_panel(
    unique_panel_id='R111-1.3',
    r_code='R111',
    version=1.3,
    gene_details='MTHFR, DHFR, FOLR1,HGNC;7436, 1:11845780-11866977, 1:11785723-11806920',
    JSON=json_data_bytes,
    BED_file_GrCH37='',
    BED_file_GrCH38='')

####################################################################################################
#function inserting new patient data

def insert_new_patient(sample_id, patient_id, unique_panel_id, date):

    new_patient = connection.execute(db.insert(samples).values(
        sample_id=sample_id,
        patient_id=patient_id,
        unique_panel_id=unique_panel_id,
        date=date))

#return a boolean indicating whether the operation was successful
    return True


new_patient_input = insert_new_patient(
    sample_id='EX135',
    patient_id='PID23',
    unique_panel_id='R111-1.3',
    date=datetime.date(2024, 1, 20))

###################################################################################################
#visualise

output = connection.execute(db.select(samples.columns)).fetchall()
output1 = connection.execute(db.select(panels.columns)).fetchall()
print(output)
print(output1)

##################################################################################################


#Function for returning JSON
#use input r_code to select panel version
def get_highest_version_json(r_code):
    # Fetch the list of unique versions for the given r_code
    list_of_versions = connection.execute(db.select(panels.columns.version).where(panels.columns.r_code == r_code))\
        .fetchall()

    # Extract the highest version number from the list if available
    if list_of_versions:
        highest_version = max(item[0] for item in list_of_versions)

    # Query the database to retrieve the JSON file associated with the highest version if available
    json_query = connection.execute(db.select(panels.columns.JSON).where((panels.columns.r_code == r_code) &
                                                                         (panels.columns.version == highest_version)))\
        .fetchone()

    return highest_version, json_query

# Example usage:
r_code_input = 'R111'  # Replace with the desired r_code
highest_version_and_json = get_highest_version_json(r_code_input)
print(highest_version_and_json)
#and 'DISCLAIMER: Unable to connect to PannelApp API, latest GMS panel provided.'
#####################################################################################################################

#retrieve patient ID and associated panel information
def retrieve_patient_and_panel_info(input_id):
    # Define the condition to match either patient_id or sample_id
    condition = or_(samples.columns.patient_id == input_id, samples.columns.sample_id == input_id)

    # Join the 'samples' and 'panels' tables on 'unique_panel_id'
    join_condition = samples.columns.unique_panel_id == panels.columns.unique_panel_id

    patient_details  = connection.execute(db.select(
        samples.columns.sample_id,
        samples.columns.patient_id,
        samples.columns.date,
        panels.columns.r_code,
        panels.columns.version,
        panels.columns.gene_details,
        panels.columns.BED_file_GrCH37,
        panels.columns.BED_file_GrCH38)\
        .select_from(samples.join(panels,
        join_condition))\
        .where(condition)).fetchall()

    # Execute the query and fetch the results
    return patient_details

patient_id_input = 'EX135'  # Replace with the desired patient_id or sample_id e.g.EX100, PID10, EX122, PID15, EX135, PID23
patient_and_panel = retrieve_patient_and_panel_info(patient_id_input)

print(patient_and_panel)

###############################################################################################################
###############################################################################################################








