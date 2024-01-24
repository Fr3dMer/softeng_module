"""*******************************************************************
File    : Database_3.0.py
About   : Generate and interact with PanelApp Database
Author  : Abi Haddon
*******************************************************************"""


import sqlalchemy as db
from sqlalchemy import MetaData, Table, Column, String, Date, Float, LargeBinary, ForeignKey, or_, and_, inspect, DateTime, Integer
from sqlalchemy.sql import select, func
import json
import datetime

# Creates a database engine using the SQLite dialect and specifies the name of the database file
# Engine is stored in the "engine" variable
# Connection to the database established using the "connect()" method of the engine.
# This is stored in the "connection" variable
# Extracting the metadata
# This line creates a MetaData object which is used to store information about the database schema
# Creates the table object named samples/panels
# Metadata creates a new meta data object which holds information about the table
# The Column() function is used to create each column, with the first argument being the name of the columm and
# the second argument being the data type
# Here, the create_all method of the metadata object is called with the engine object as an argument
# This creates the tables in the database

class PanelAppDB:
    def __init__(self, db_url='sqlite:///panel_app_db.db'):
        self.engine = db.create_engine(db_url)
        self.connection = self.engine.connect()
        self.metadata = MetaData()

        self.samples = Table('samples', self.metadata,
                             Column('sample_id', String(255), primary_key=True, nullable=False),
                             Column('patient_id', String(255), nullable=False),
                             Column('unique_panel_id', String(255), ForeignKey('panels.unique_panel_id'), nullable=False),
                             Column('date', DateTime, default=func.now())
                             )

        self.panels = Table('panels', self.metadata,
                            Column('unique_panel_id', String(255), primary_key=True, nullable=False),
                            Column('panelapp_panel_id', Integer, nullable=False),
                            Column('r_code', String(255)),
                            Column('version', Float(), nullable=False),
                            Column('gene_details', String(255), nullable=False),
                            Column('JSON', LargeBinary),
                            Column('BED_file_GrCH37', String),
                            Column('BED_file_GrCH38', String),
                            )

        # Check if tables exist before creating them - preventing data loss
        inspector = inspect(self.engine)
        if not inspector.has_table('samples') or not inspector.has_table('panels'):
            self.metadata.create_all(self.engine)

# Use the table object to run the query and extract the results
# The query is executed using a database connection object called connection
# using the select method, to select all columns in the samples table - use the columns
# attribute of the table to get the columns and pass that to the select function
# the results of the query are stored in the output variable

# Functions for inserting new patient record into the samples table

    def insert_patient_record(self, sample_id, patient_id, unique_panel_id, date):
        query = self.connection.execute(db.insert(self.samples).values(
                sample_id=sample_id,
                patient_id=patient_id,
                unique_panel_id=unique_panel_id,
                date=date
            ))
        return True

#Function for inserting a new version of a GMS panel
#Check version of panel present in database
#return a boolean indicating whether the operation was successful
    def insert_panel_record_rcode(self, unique_panel_id, panelapp_panel_id, r_code, version, gene_details, JSON, BED_file_GrCH37, BED_file_GrCH38):

        list_of_version = [item[0] for item in self.connection.execute(db.select(self.panels.columns.version)
                        .where(self.panels.columns.r_code == r_code)).fetchall()]

        if version not in list_of_version:
            query = self.connection.execute(db.insert(self.panels).values(
                unique_panel_id=unique_panel_id,
                panelapp_panel_id=panelapp_panel_id,
                r_code=r_code,
                version=version,
                gene_details=gene_details,
                JSON=JSON,
                BED_file_GrCH37=BED_file_GrCH37,
                BED_file_GrCH38=BED_file_GrCH38
            ))
            return True
        else:
            print("Panel with the same r_code and version already exists")
            return False

    def insert_panel_record_panelid(self, unique_panel_id, panelapp_panel_id, r_code, version, gene_details, JSON, BED_file_GrCH37, BED_file_GrCH38):

        list_of_version = [item[0] for item in self.connection.execute(db.select(self.panels.columns.version)
                        .where(self.panels.columns.panelapp_panel_id == panelapp_panel_id)).fetchall()]

        if version not in list_of_version:
            query = self.connection.execute(db.insert(self.panels).values(
                unique_panel_id=unique_panel_id,
                panelapp_panel_id=panelapp_panel_id,
                r_code=r_code,
                version=version,
                gene_details=gene_details,
                JSON=JSON,
                BED_file_GrCH37=BED_file_GrCH37,
                BED_file_GrCH38=BED_file_GrCH38
            ))
            return True
        else:
            print("Panel with the same r_code and version already exists")
            return False

#Function for returning JSON when internet connection fails
#use input r_code to select highest panel version

    def retrieve_highest_version_json_panel_id(self, panelapp_panel_id):
        list_of_versions = self.connection.execute(db.select(self.panels.columns.version)
            .where(self.panels.columns.panelapp_panel_id == panelapp_panel_id)).fetchall()

      #  The if statement is checking whether the list_of_versions is not empty.In Python, an empty
      #  list evaluates to False in a boolean context, and a non - empty list evaluates to True

        if list_of_versions:
            highest_version = max(item[0] for item in list_of_versions)
            json_query = self.connection.execute(db.select(self.panels.columns.JSON)
                .where((self.panels.columns.panelapp_panel_id == panelapp_panel_id) & (self.panels.columns.version == highest_version))).fetchone()
            return json_query
        else:
            return None

    def retrieve_highest_version_json_rcode(self, r_code):
        list_of_versions = self.connection.execute(db.select(self.panels.columns.version)
            .where(self.panels.columns.r_code == r_code)).fetchall()

        if list_of_versions:
            highest_version = max(item[0] for item in list_of_versions)
            json_query = self.connection.execute(db.select(self.panels.columns.JSON)
                .where((self.panels.columns.r_code == r_code) & (self.panels.columns.version == highest_version))).fetchone()
            return json_query
        else:
            return None

#retrieve patient ID and associated panel information
#condition defined to match either patient_id or sample_id

    def retrieve_patient_and_panel_info(self, input_id):

        condition = or_(self.samples.columns.patient_id == input_id, self.samples.columns.sample_id == input_id)
        join_condition = self.samples.columns.unique_panel_id == self.panels.columns.unique_panel_id

        ######## TODO:add way of checking patient_id and sample_id aren't the same' ########

        patient_details = self.connection.execute(db.select(
            self.samples.columns.sample_id,
            self.samples.columns.patient_id,
            self.samples.columns.date,
            self.panels.columns.panelapp_panel_id,
            self.panels.columns.r_code,
            self.panels.columns.version,
            self.panels.columns.gene_details,
            self.panels.columns.BED_file_GrCH37,
            self.panels.columns.BED_file_GrCH38)
            .select_from(self.samples.join(self.panels, join_condition))
            .where(condition)).fetchall()

        return patient_details


if (__name__ == "__main__"):

    # Example usage:
    db_manager = PanelAppDB()

    db_manager.insert_patient_record('EX100', 'PID10', 'R111-1.1-1', datetime.date(2023, 12, 10))
    db_manager.insert_patient_record('EX122', 'PID15', 'R111-1.2-1', datetime.date(2024, 1, 18))
    db_manager.insert_patient_record('EX135', 'PID23', 'R111-1.3-1', datetime.date(2024, 1, 20))
    db_manager.insert_patient_record('EX147', 'PID32', 'R111-1.4-1', datetime.date(2024, 1, 24))


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

    db_manager.insert_panel_record_rcode('R111-1.1-1', 1, 'R111', 1.1, 'MTHFR, HGNC;7436, 1:11845780-11866977, 1:11785723-11806920', json_data_bytes, '', '')
    db_manager.insert_panel_record_rcode('R111-1.2-1', 1, 'R111', 1.2, 'MTHFR, DHFR, HGNC;7436, 1:11845780-11866977, 1:11785723-11806920', json_data_bytes, '', '')
    db_manager.insert_panel_record_rcode('R111-1.3-1', 1, 'R111', 1.3, 'MTHFR, DHFR, HGNC;7436, 1:11845780-11866977, 1:11785723-11806920', json_data_bytes, '', '')

    db_manager.insert_panel_record_panelid('R111-1.4-1', 1, None, 1.4,'MTHFR, DHFR, HGNC;7436, 1:11845780-11866977, 1:11785723-11806920', json_data_bytes, '', '')

    patient_and_panel_info = db_manager.retrieve_patient_and_panel_info('EX122')
    # Replace with the desired patient_id or sample_id e.g.EX100, PID10, EX122, PID15, EX135, PID23
    print(patient_and_panel_info)

    highest_version_and_json_panel_id = db_manager.retrieve_highest_version_json_panel_id('1')
    print(highest_version_and_json_panel_id)

    highest_version_and_json_rcode = db_manager.retrieve_highest_version_json_rcode('R111')
    print(highest_version_and_json_rcode)
    ######## TODO: add 'DISCLAIMER: Unable to connect to PannelApp API, latest GMS panel provided.' ########

    output = db_manager.connection.execute(db.select(db_manager.samples.columns)).fetchall()
    output1 = db_manager.connection.execute(db.select(db_manager.panels.columns)).fetchall()
    print(output)
    print(output1)




