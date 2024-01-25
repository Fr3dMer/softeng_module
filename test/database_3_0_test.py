"""***************************************************************************
File          : database_3.0_test.py
About         : Test db class is working as expected 
Author        : Freddie Mercer
Date modified : 2024-01-25
***************************************************************************"""

import pytest
import shutil
import os.path
import datetime
import src.database_3_0 as db 

info_str = 'MTHFR, HGNC;7436, 1:11845780-11866977, 1:11785723-11806920'


@pytest.fixture
def db_env():
    # Create fixture to automate db creation and deletion 
    
    db_folder = "tmp_test"
    os.mkdir(db_folder)
    db_url = 'sqlite:///tmp_test/panel_app_db.db'
    db_obj = db.PanelAppDB(db_url)

    yield db_obj
    
    db_obj.connection.close() 
    if (os.path.exists(db_folder)):
        shutil.rmtree(db_folder)    


def test_insert_patient_record(db_env):
    # Test insert patient record func
    
    assert os.path.exists("tmp_test") == True
    assert db_env.insert_patient_record('EX100', 
                                        'PID10', 
                                        'R111-1.1-1', 
                                        datetime.date(2023, 12, 10)) == True


def test_insert_panel_record_rcode(db_env):
    # Test insert_panel_record_rcode func 
    
    assert db_env.insert_panel_record_rcode('R111-1.1-1', 
                                            1, 
                                            'R111', 
                                            1.1, 
                                            info_str, 
                                            b'json_data', 
                                            '', 
                                            '') == True


def test_insert_panel_record_panelid(db_env):
    # Test insert_panel_record_panelid func
    
    assert db_env.insert_panel_record_panelid('R111-1.4-1', 
                                              1, 
                                              None, 
                                              1.4,
                                              info_str, 
                                              b'json_data', 
                                              '', 
                                              '') == True


def test_retrieve_highest_version_json_panel_id(db_env):
    # Test retrieve_highest_version_json_panel_id func
    
    db_env.insert_panel_record_panelid('R111-1.5-1', 
                                       1, 
                                       None, 
                                       1.5,
                                       info_str, 
                                       b'1.5', 
                                       '', 
                                       '')
    db_env.insert_panel_record_panelid('R111-1.4-1', 
                                       1, 
                                       None, 
                                       1.4,
                                       info_str, 
                                       b'1.4', 
                                       '', 
                                       '')

    result = db_env.retrieve_highest_version_json_panel_id('1')
    assert result == (b'1.5',)


def test_retrieve_highest_version_json_rcode(db_env):
    # Test retrieve_highest_version_json_rcode func

    db_env.insert_panel_record_panelid('R111-1.5-1', 
                                       1, 
                                       'R111', 
                                       1.5,
                                       info_str, 
                                       b'1.5', 
                                       '', 
                                       '') 
    db_env.insert_panel_record_panelid('R111-1.4-1', 
                                       1, 
                                       'R111', 
                                       1.4,
                                       info_str, 
                                       b'1.4', 
                                       '', 
                                       '') 
    
    result = db_env.retrieve_highest_version_json_rcode('R111')
    assert result == (b'1.5',)


def test_retrieve_patient_and_panel_info(db_env):
    # Test retrieve_patient_and_panel_info func

    result = db_env.retrieve_patient_and_panel_info('EX122')
    assert result is not None
