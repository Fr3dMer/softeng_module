"""***************************************************************************
File          : JSON_parsing.py
About         : Ensure JSON are parsed as expected 
Author        : Freddie Mercer
Date modified : 2023-12-01
***************************************************************************"""

import json
import pytest
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


class TestJSON_parsing():

#-----------------------------------------------------------------------------
# 					     extract_panel_id test 
# 	Function: extract pannel id from JSON
# 	Tests: Can it deal with normal JSON and when its not present?
#-----------------------------------------------------------------------------
    def test_json1_extract_panel_id (self,json_obj,normal_json):

        assert json_obj.extract_panel_id(normal_json) == 504

        # Does it raise errors as expected?
        assert json_obj.extract_panel_id(empty_json) == 'Nan'