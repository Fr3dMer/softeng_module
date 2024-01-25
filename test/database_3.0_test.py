"""***************************************************************************
File          : database_3.0_test.py
About         : Test db class is working as expected 
Author        : Freddie Mercer
Date modified : 2024-01-25
***************************************************************************"""

import pytest
import src.database_3_0 as db 

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
