"""***************************************************************************
File          : api_test.py
About         : Test API wrapper/interface works as expected, no need to
                    test actual API as otherwise this becomes an integration 
                    test. Instead only checker will be tested, maybe worth 
                    seperating from actual api calls?
Author        : Freddie Mercer
Date modified : 2023-12-08
***************************************************************************"""

import pytest
import src.api as api_obj

#-----------------------------------------------------------------------------
# Setup test enviro 
#-----------------------------------------------------------------------------
@pytest.fixture
def api_setup():
    yield api_obj.api_obj("args")


class TestApi():

#-----------------------------------------------------------------------------
#                   get_gms_pannel test 
# 	Function: Funcs goal is to ensure values are correct type before being
#               used for api call
# 	Tests: Test no params does not raise error, test correct formating of
#           pannel_id,version and rcode data types
#-----------------------------------------------------------------------------
    def test_api1_value_checker(self,api_setup):

        # No params
        assert api_setup.value_checker() == None

        # Normal panel id 
        p_id = 123
        assert api_setup.value_checker(pannel_id = p_id) == None
        
        # Incorrect panel id's
        str_p_id = '123'
        float_p_id = 1.23
        with pytest.raises(SystemError):
            assert api_setup.value_checker(pannel_id = str_p_id)
        with pytest.raises(SystemError):
            assert api_setup.value_checker(pannel_id = float_p_id)

        # Normal version (can be str or float) 
        str_ver = '1.2'
        float_ver = 1.2
        assert api_setup.value_checker(version = str_ver) == None
        assert api_setup.value_checker(version = float_ver) == None

        # Incorrect version type
        with pytest.raises(SystemError):
            assert api_setup.value_checker(version = p_id)

        # Normal rcode 
        str_rcode = 'R123'
        assert api_setup.value_checker(rcode = str_rcode) == None

        # Incorrect rcode type
        with pytest.raises(SystemError):
            assert api_setup.value_checker(rcode = p_id)


#-----------------------------------------------------------------------------
#                   version_check test 
# 	Function: wants to compare versions of panels
# 	Tests: Are the variables entered comparable and does comparison work
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
        

