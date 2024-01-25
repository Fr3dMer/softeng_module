"""***************************************************************************
File          : api_test.py
About         : Test API wrapper/interface works as expected, api calls
                  intercepted through responses lib 
Author        : Freddie Mercer
Date modified : 2023-12-20
***************************************************************************"""

import json
import pytest
import responses
import src.api as api_obj
import src.logging_1_0 as log_obj

#-----------------------------------------------------------------------------
# Setup test enviro 
#-----------------------------------------------------------------------------
@pytest.fixture
def api_setup():
    yield api_obj.api_obj(log_obj.LoggerManager())

@pytest.fixture
def normal_json():
    f = open("test/JSON_test_data.json")
    normal_json = json.load(f)
    f.close
    yield normal_json

@pytest.fixture
def gms_data_json():
    f = open("test/signed_off_gms.json")
    gms_data_json = json.load(f)
    f.close
    yield gms_data_json

@pytest.fixture
def gms_json():
    f = open("test/JSON_test_data2.json")
    gms_json = json.load(f)
    f.close
    yield gms_json

# Setup responses to catch calls by requests
@pytest.fixture
def response(normal_json,gms_data_json,gms_json):

    base = "https://panelapp.genomicsengland.co.uk/api/v1/panels/"

    resp1 = responses.Response(
            method = "GET",
            url = base + "504",
            json = normal_json,
            status = 200,
        )
    resp2 = responses.Response(
            method = "GET",
            url = base + "504/?version=2.0",
            json = gms_json,
            status = 200,
        )
    resp3 = responses.Response(
            method = "GET",
            url = base + "signedoff/504",
            json = gms_data_json,
            status = 200,
        )
    resp4 = responses.Response(
            method = "GET",
            url = base + "R211",
            json = normal_json,
            status = 200,
        )
    responses.add(resp1)
    responses.add(resp2)
    responses.add(resp3)
    responses.add(resp4)
    

class TestApi():

#-----------------------------------------------------------------------------
#                   get_gms_pannel test 
#  Function: Funcs goal is to ensure values are correct type before being
#               used for api call
#  Tests: Test no params does not raise error, test correct formating of
#           pannel_id,version and rcode data types
#-----------------------------------------------------------------------------
    def test_api1_value_checker(self,api_setup):

        # No params
        assert api_setup.value_checker() == None

        # Normal panel id 
        p_id = 123
        assert api_setup.value_checker(panel_id = p_id) == None
        
        # Incorrect panel id's
        str_p_id = '123'
        float_p_id = 1.23
        with pytest.raises(ValueError):
            assert api_setup.value_checker(panel_id = str_p_id)
        with pytest.raises(ValueError):
            assert api_setup.value_checker(panel_id = float_p_id)

        # Normal version (can be str or float) 
        str_ver = '1.2'
        float_ver = 1.2
        assert api_setup.value_checker(version = str_ver) == None
        assert api_setup.value_checker(version = float_ver) == None

        # Incorrect version type
        with pytest.raises(ValueError):
            assert api_setup.value_checker(version = p_id)

        # Normal rcode 
        str_rcode = 'R123'
        assert api_setup.value_checker(rcode = str_rcode) == None

        # Incorrect rcode type
        with pytest.raises(ValueError):
            assert api_setup.value_checker(rcode = p_id)


#-----------------------------------------------------------------------------
#                   version_check test 
#  Function: wants to compare versions of panels
#  Tests: Are the variables entered comparable and does comparison work
#-----------------------------------------------------------------------------
    def test_api2_version_check(self,api_setup):

        # Can it detect incorect var types
        wrong_type = '1.23'
        right_type = 1.23
        with pytest.raises(SyntaxError):
            api_setup.version_check(wrong_type,right_type)
        with pytest.raises(SyntaxError):
            api_setup.version_check(right_type,wrong_type)
        
        # Does it work? 
        assert api_setup.version_check(right_type,right_type) == True

        assert api_setup.version_check(right_type,1.4) == False
        

#-----------------------------------------------------------------------------
#                   check_internet test 
#  Function: ensure there is an actual internet connection
#  Tests: Using a normla and garbled url, does it return correct bools
#-----------------------------------------------------------------------------
    def test_api3_check_internet(self,api_setup):

        norm_url = 'http://google.com'
        bad_url = '192.0.2.0/24'

        assert api_setup.check_internet(norm_url) == True
        assert api_setup.check_internet(bad_url) == False


#-----------------------------------------------------------------------------
#                   get_gms_pannel test 
#  Function: get most recently signed off GMS pannel
#  Tests: ensure URL correctly formated and called
#-----------------------------------------------------------------------------
    @responses.activate
    def test_api4_get_gms_pannel(self,api_setup,gms_data_json,response):

        id = 504

        assert api_setup.get_gms_pannel(id) == gms_data_json


#-----------------------------------------------------------------------------
#                   get_single_detailed_pannel_id test 
#  Function: call API and return parsed JSON, can specify version 
#  Tests: Normal function with and withought version
#-----------------------------------------------------------------------------
    @responses.activate
    def test_api5_get_single_detailed_pannel_id(self,
                                                api_setup,
                                                normal_json,
                                                gms_json,
                                                response):
        
        id = 504
        ver = 2.0

        # No version
        assert api_setup.get_single_detailed_pannel_id(id) == normal_json

        # With version
        assert api_setup.get_single_detailed_pannel_id(id,ver) == gms_json


#-----------------------------------------------------------------------------
#                   get_single_detailed_pannel_rcode test 
#  Function: call api by rcode and return correct data  
#  Tests: Normal functioning
#-----------------------------------------------------------------------------
    @responses.activate
    def test_api6_get_single_detailed_pannel_rcode(self,
                                                   api_setup,
                                                   normal_json,
                                                   response):

        rcode = "R211"

        # No version
        assert api_setup.get_single_detailed_pannel_rcode(rcode) == normal_json