# script created using the following websites:
# https://www.datacamp.com/tutorial/sqlalchemy-tutorial-examples
# https://towardsdatascience.com/sqlalchemy-python-tutorial-79a577141a91
# https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#declaring-simple-constraints

import sqlalchemy as db
from sqlalchemy import MetaData, Table, Column, String, Date, Float, LargeBinary, ForeignKey
import pandas as pd
import datetime

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
                  db.Column('HGNC_id', db.String(255), nullable=False),
                  db.Column('genes', db.String(255), nullable=False),
                  db.Column('reference_sequence_GrCH37', db.String(255)),
                  db.Column('reference_sequence_GrCH38', db.String(255)),
                  db.Column('JSON', LargeBinary),
                  db.Column('BED_file', String),
                  )
# Creates the table object named panels
# Metadata creates a new meta data objet which holds information about the table
# The Column() function is used to create each column, with the first argument being the name of the columm and the second argument being the data type


metadata.create_all(engine)
#metadata.drop_all(engine)
# Here, the create_all method of the metadata object is called with the engine object as an argument
# This creates the tables in the database


print("Columns in 'samples' table:", samples.columns.keys())
print("Columns in 'panels' table:", panels.columns.keys())
# Print information about the 'samples' table columns

query = db.insert(samples).values(sample_id='EX100', patient_id='PID10', unique_panel_id='101', date=datetime.date(2023, 12, 10))
record = connection.execute(query)

query = db.insert(panels).values(unique_panel_id='101', r_code='R111', version='1.1', HGNC_id='HGNC;7436', genes='MTHFR', reference_sequence_GrCH37='1:11845780-11866977', reference_sequence_GrCH38='1:11785723-11806920', BED_file='')
record = connection.execute(query)
# Inserting record one by one

output = connection.execute(db.select(samples.columns)).fetchall()
# Use the table object to run the query and extract the results
# The query is executed using a database connection object called connection
# using the select method, to select all columns in the samples table - use the columns attribute of the table to get the columns and pass that to the select function
# the results of the query are stored in the output variable

# Check if there are rows returned
if output:
    # Get column names from the first row
    column_names = samples.columns.keys()

    # Convert the result to a DataFrame
    data = pd.DataFrame(output, columns=column_names)

    # Display the panda dataFrame
    print(data)
else:
    print("No data returned.")
