"""***************************************************************************
File          : api_test.py
About         : Test API works as expected 
Author        : Freddie Mercer
Date modified : 2023-12-01
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
# 					     get_gms_pannel test 
# 	Function: Funcs goal is getting GMS signed off pannel details. How do 
#			    test an API that is regularily changing is returning the 
#  				correct/expected data?
# 	Tests: Normal request, non-existent pannel id, none type
#-----------------------------------------------------------------------------
	def test_api1_get_gms_pannel(self,api_setup):
		
		# Normal
		test_id = 1
		assert "" == api_setup.get_gms_pannel(test_id)
		


