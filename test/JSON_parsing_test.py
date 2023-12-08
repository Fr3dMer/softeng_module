"""***************************************************************************
File          : JSON_parsing.py
About         : Ensure JSON are parsed as expected 
Author        : Freddie Mercer
Date modified : 2023-12-01

TODO: Need to capture logs once logging implemented
***************************************************************************"""

import json
import pytest
import numpy as np
import src.JSON_parsing as JSON_obj

#-----------------------------------------------------------------------------
# Setup test enviro 
#-----------------------------------------------------------------------------

empty_json = {"":"","":""}

@pytest.fixture
def normal_json():
    f = open("test/JSON_test_data.json")
    normal_json = json.load(f)
    f.close
    yield normal_json

@pytest.fixture
def json_obj():
    yield JSON_obj.Parser("args")

gene_list = ['HGNC:583', 
             'HGNC:1076', 
             'HGNC:11529', 
             'HGNC:7127', 
             'HGNC:7325', 
             'HGNC:7329', 
             'HGNC:7527', 
             'HGNC:8028', 
             'HGNC:9122', 
             'HGNC:9175', 
             'HGNC:9177', 
             'HGNC:9588', 
             'HGNC:18505', 
             'HGNC:6770', 
             'HGNC:11389', 
             'HGNC:904', 
             'HGNC:2001', 
             'HGNC:6919', 
             'HGNC:7326'] 

class TestJSON_parsing():

#-----------------------------------------------------------------------------
# 					     extract_panel_id test 
# 	Function: extract pannel id from JSON
# 	Tests: Can it deal with normal JSON and when its not present?
#-----------------------------------------------------------------------------
    def test_json1_extract_panel_id (self,json_obj,normal_json):

        # Normal
        assert json_obj.extract_panel_id(normal_json) == 504

        # Does it raise errors as expected?
        assert np.isnan(json_obj.extract_panel_id(empty_json)) == True


#-----------------------------------------------------------------------------
# 					     extract_version test 
# 	Function: extract version from json
# 	Tests: Can it deal with normal JSON and when its not present?
#-----------------------------------------------------------------------------
    def test_json2_extract_panel_id(self,json_obj,normal_json):

        # Normal
        assert json_obj.extract_version(normal_json) == '2.8'

        # Does it raise errors as expected?
        assert np.isnan(json_obj.extract_version(empty_json)) == True


#-----------------------------------------------------------------------------
# 					     extract_disease test 
# 	Function: extract associated dieases with test
# 	Tests: Can it deal with normal JSON and when its not present?
#-----------------------------------------------------------------------------
    def test_json3_extract_disease(self,json_obj,normal_json):

        # Normal
        assert json_obj.extract_disease(normal_json) == ['Inherited ' + \
                                                         'polyposis', 
                                                         'R211']

        # Does it raise errors as expected?
        assert np.isnan(json_obj.extract_disease(empty_json)) == True


#-----------------------------------------------------------------------------
#                        extract_last_updated test 
#   Function: extract date the panel was last updated
#   Tests: Can it deal with normal JSON and when its not present?
#-----------------------------------------------------------------------------
    def test_json3_extract_last_updated(self,json_obj,normal_json):

        # Normal
        assert json_obj.extract_last_updated(normal_json) == '2023-10-26'

        # Does it raise errors as expected?
        assert np.isnan(json_obj.extract_last_updated(empty_json)) == True


#-----------------------------------------------------------------------------
#                        extract_genes test 
#   Function: extract genes present and return as a list
#   Tests: Can it deal with normal JSON and when its not present?
#-----------------------------------------------------------------------------
    def test_json4_extract_genes(self,json_obj,normal_json):

        # Normal
        assert json_obj.extract_genes(normal_json) == gene_list

        # Does it raise errors as expected?
        assert np.isnan(json_obj.extract_genes(empty_json)) == True