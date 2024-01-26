"""*******************************************************************
File    : Database_3_0.py
About   : Generate and interact with PanelApp Database
Author  : Abi Haddon
*******************************************************************"""


import sqlalchemy as db
from sqlalchemy import (MetaData, Table, Column, String, Float, LargeBinary,
                        ForeignKey, or_, inspect, DateTime, Integer)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func
import src.logging as logger
import json
import datetime


class PanelAppDB:
    """
    A class for interacting with the PanelApp database.

    Attributes:
        engine: A SQLAlchemy engine instance representing the core interface
        to the database.
        connection: A SQLAlchemy connection instance representing the active
        connection to the database.
        metadata: A SQLAlchemy MetaData instance which stores information about
        the database schema.
        samples: A SQLAlchemy Table instance representing the 'samples' table
        in the database.
        panels: A SQLAlchemy Table instance representing the 'panels' table
        in the database.

    Methods:
        __init__(self, db_url='sqlite:///panel_app_db.db'): Initializes the
        PanelAppDB instance.

        insert_patient_record(self, sample_id, patient_id, unique_panel_id,
        date): Inserts a new patient record into the 'samples' table.

        insert_panel_record_rcode(self, unique_panel_id, panelapp_panel_id,
        r_code, version, gene_details, JSON, BED_file_GrCH37, BED_file_GrCH38):
        Inserts a new panel record into the 'panels' table based on r_code.

        insert_panel_record_panelid(self, unique_panel_id, panelapp_panel_id,
        r_code, version, gene_details, JSON, BED_file_GrCH37, BED_file_GrCH38):
        Inserts a new panel record into the 'panels' table based on
        panelapp_panel_id.

        retrieve_highest_version_json_panel_id(self,
        panelapp_panel_id): Retrieves the highest version of a panel based
        on panelapp_panel_id.

        retrieve_highest_version_json_rcode(self, r_code): Retrieves the
        highest version of a panel based on r_code.

        retrieve_patient_and_panel_info(self, input_id): Retrieves patient
        and panel information based on input_id.
    """

    def __init__(self, db_url='sqlite:///panel_app_db.db'):
        """
        Initialize the PanelAppDB instance.

        Parameters:
            db_url (str): Default database URL: 'sqlite:///panel_app_db.db'.
        """
        try:
            # Creates a database engine
            self.engine = db.create_engine(db_url)
            # Connect to the database established using the 'connect()' method
            self.connection = self.engine.connect()
            # MetaData object stores information about the database schema
            self.metadata = MetaData()

            # The Column() function is used to create each column
            self.samples = Table('samples', self.metadata,
                                 Column('sample_id', String(255),
                                        primary_key=True, nullable=False),
                                 Column('patient_id', String(255),
                                        nullable=False),
                                 Column('unique_panel_id', String(255),
                                        ForeignKey('panels.unique_panel_id'),
                                        nullable=False),
                                 Column('date', DateTime, default=func.now())
                                 )

            self.panels = Table('panels', self.metadata,
                                Column('unique_panel_id', String(255),
                                       primary_key=True, nullable=False),
                                Column('panelapp_panel_id', Integer,
                                       nullable=False),
                                Column('r_code', String(255)),
                                Column('version', Float(), nullable=False),
                                Column('gene_details', String(255),
                                       nullable=False),
                                Column('JSON', LargeBinary),
                                Column('BED_file_GrCH37', String),
                                Column('BED_file_GrCH38', String),
                                )

            # Check if tables exist before creating them - preventing data loss
            inspector = inspect(self.engine)
            if not inspector.has_table('samples') or not inspector.has_table(
                    'panels'):

                # The create_all method creates the tables in the database
                self.metadata.create_all(self.engine)
        except SQLAlchemyError as e:
            logger.exception(f"Error occurred when initialising database: {e}")

    def insert_patient_record(self, sample_id, patient_id,
                              unique_panel_id, date):
        """
        Insert a new patient record into the 'samples' table.

        Parameters:
            sample_id (str): The sample ID.
            patient_id (str): The patient ID.
            unique_panel_id (str): The unique panel ID.
            date (datetime.date): The date.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        try:
            # Query is executed using a database connection object
            self.connection.execute(db.insert(self.samples).values(
                sample_id=sample_id,
                patient_id=patient_id,
                unique_panel_id=unique_panel_id,
                date=date
            ))
            return True
        except SQLAlchemyError as e:
            logger.exception(f"Error occurred inserting patient record: {e}")
            return False

    def insert_panel_record_rcode(self, unique_panel_id, panelapp_panel_id,
                                  r_code, version, gene_details, JSON,
                                  BED_file_GrCH37, BED_file_GrCH38):
        """
        Insert a new panel record into the 'panels' table based on r_code.

        Parameters:
            unique_panel_id (str): The unique panel ID.
            panelapp_panel_id (int): The panelapp panel ID.
            r_code (str): The r_code.
            version (float): The version.
            gene_details (str): The gene details.
            JSON (LargeBinary): The JSON data.
            BED_file_GrCH37 (str): The BED file for GrCh37.
            BED_file_GrCH38 (str): The BED file for GrCh38.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        try:
            # Get list of versions using r_code
            list_of_version = [item[0] for item in self.connection.execute(
                db.select(self.panels.columns.version)
                .where(
                    self.panels.columns.r_code == r_code)).fetchall()]

            # Insert new record if version not present
            if version not in list_of_version:
                self.connection.execute(db.insert(self.panels).values(
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
        except SQLAlchemyError as e:
            logger.exception(f"Error occurred when inserting "
                             f"panel record based on r_code: {e}")
            return False

    def insert_panel_record_panelid(self, unique_panel_id, panelapp_panel_id,
                                    r_code, version, gene_details, JSON,
                                    BED_file_GrCH37, BED_file_GrCH38):
        """
        Insert a new panel record into the 'panels' table based on
        panelapp_panel_id.

        Parameters:
            unique_panel_id (str): The unique panel ID.
            panelapp_panel_id (int): The panelapp panel ID.
            r_code (str): The r_code.
            version (float): The version.
            gene_details (str): The gene details.
            JSON (LargeBinary): The JSON data.
            BED_file_GrCH37 (str): The BED file for GrCh37.
            BED_file_GrCH38 (str): The BED file for GrCh38.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        try:
            # Get list of versions using panelapp_panel_id
            list_of_version = [item[0] for
                               item in self.connection.execute(db.select(
                                    self.panels.columns.version)
                    .where(
                        self.panels.columns
                        .panelapp_panel_id == panelapp_panel_id))
                                   .fetchall()]

            # Insert new record if version not present
            if version not in list_of_version:
                self.connection.execute(db.insert(self.panels).values(
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
        except SQLAlchemyError as e:
            logger.exception(f"Error occurred trying to insert panel record "
                             f"when using panelapp_id : {e}")
            return False

    def retrieve_highest_version_json_panel_id(self, panelapp_panel_id):
        """
        Retrieve the highest version of a panel based on panelapp_panel_id.

        Parameters:
            panelapp_panel_id (int): The panelapp panel ID.

        Returns:
            tuple: The highest version and JSON data of the panel,
            or None if no such panel exists.
        """
        try:
            # Get list of versions using panelapp_panel_id
            list_of_versions = self.connection.execute(db.select(
                    self.panels.columns.version)
                .where(
                    self.panels.columns
                    .panelapp_panel_id == panelapp_panel_id)).fetchall()

            # Use highest version to return json
            if list_of_versions:
                highest_version = max(item[0] for item in list_of_versions)
                json_query = self.connection.execute(

                    # Select columns in table using select method
                    db.select(self.panels.columns.JSON).where(
                        (self.panels.columns
                            .panelapp_panel_id == panelapp_panel_id) & (
                                self.panels.columns
                                .version == highest_version)))\
                    .fetchone()
                return json_query
            else:
                return None
        except SQLAlchemyError as e:
            logger.exception(f"Error occurred when trying to retrieve json "
                             f"using panelapp_id: {e}")
            return None

    def retrieve_highest_version_json_rcode(self, r_code):
        """
        Retrieve the highest version of a panel based on r_code.

        Parameters:
            r_code (str): The r_code.

        Returns:
            tuple: The highest version and JSON data of the panel,
            or None if no such panel exists.
        """
        try:
            # Get list of versions using r_code
            list_of_versions = self.connection.execute(
                db.select(self.panels.columns.version)
                .where(self.panels.columns.r_code == r_code)).fetchall()

            # Use highest version to return json
            if list_of_versions:
                highest_version = max(item[0] for item in list_of_versions)
                json_query = self.connection.execute(
                    # Select columns in table using select method
                    db.select(self.panels.columns.JSON)
                    .where((self.panels.columns.r_code == r_code) & (
                            self.panels.columns.version == highest_version)))\
                    .fetchone()
                return json_query
            else:
                return None
        except SQLAlchemyError as e:
            logger.exception(f"Error occurred when trying to retrieve"
                             f" json using r_code: {e}")
            return None

    def retrieve_patient_and_panel_info(self, input_id):
        """
        Retrieve patient and panel information based on input_id.

        Parameters:
            input_id (str): The input ID, which could be either a
            patient_id or a sample_id.

        Returns:
            list: A list of tuples containing the patient and panel
            information, or an empty list if no such patient or sample exists.
        """
        try:
            # Select rows on whether either the patient_id or
            # the sample_id matches the input_id
            condition = or_(self.samples.columns.patient_id == input_id,
                            self.samples.columns.sample_id == input_id)
            # join rows from two tables
            join_condition = self.samples.columns.unique_panel_id == \
                self.panels.columns.unique_panel_id

            # TODO: add checking patient_id and sample_id
            # aren't the same'

            # select required columns
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
        except SQLAlchemyError as e:
            logger.exception(f"Error occurred when trying to "
                             f"retrieve panel and patient info: {e}")
            return []


if (__name__ == "__main__"):
    try:
        # Example usage of database
        db_manager = PanelAppDB()

        # inserting data into samples table
        db_manager.insert_patient_record('EX100', 'PID10',
                                         'R111-1.1-1',
                                         datetime.date(2023, 12, 10))
        db_manager.insert_patient_record('EX122', 'PID15',
                                         'R111-1.2-1',
                                         datetime.date(2024, 1, 18))
        db_manager.insert_patient_record('EX135', 'PID23',
                                         'R111-1.3-1',
                                         datetime.date(2024, 1, 20))
        db_manager.insert_patient_record('EX147', 'PID32',
                                         'R111-1.4-1',
                                         datetime.date(2024, 1, 24))

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

        # inserting data into panels table
        db_manager.insert_panel_record_rcode('R111-1.1-1', 1, 'R111', 1.1,
                                             'MTHFR, HGNC;7436, '
                                             '1:11845780-11866977, '
                                             '1:11785723-11806920',
                                             json_data_bytes, '', '')
        db_manager.insert_panel_record_rcode('R111-1.2-1', 1, 'R111', 1.2,
                                             'MTHFR, DHFR, HGNC;7436, '
                                             '1:11845780-11866977, '
                                             '1:11785723-11806920',
                                             json_data_bytes, '', '')
        db_manager.insert_panel_record_rcode('R111-1.3-1', 1, 'R111', 1.3,
                                             'MTHFR, DHFR, HGNC;7436, '
                                             '1:11845780-11866977, '
                                             '1:11785723-11806920',
                                             json_data_bytes, '', '')

        db_manager.insert_panel_record_panelid('R111-1.4-1', 1, None, 1.4,
                                               'MTHFR, DHFR, HGNC;7436, '
                                               '1:11845780-11866977, '
                                               '1:11785723-11806920',
                                               json_data_bytes, '', '')

        # return required information
        patient_and_panel_info = db_manager.retrieve_patient_and_panel_info(
            'EX122')
        # Replace with the desired patient_id or sample_id e.g.EX100,
        # PID10, EX122, PID15, EX135, PID23
        print(patient_and_panel_info)

        highest_version_and_json_panel_id = db_manager\
            .retrieve_highest_version_json_panel_id('1')
        print(highest_version_and_json_panel_id)

        highest_version_and_json_rcode = db_manager\
            .retrieve_highest_version_json_rcode('R111')
        print(highest_version_and_json_rcode)
        # TODO: add 'DISCLAIMER: Unable to connect
        # to PannelApp API, latest GMS panel provided.'

        output = db_manager.connection.execute(db.select(
            db_manager.samples.columns)).fetchall()
        output1 = db_manager.connection.execute(db.select(
            db_manager.panels.columns)).fetchall()
        print(output)
        print(output1)

    except Exception as e:
        print("An error occurred within the execution block:", str(e))
    finally:
        # Close the database connection
        if db_manager is not None:
            db_manager.connection.close()
