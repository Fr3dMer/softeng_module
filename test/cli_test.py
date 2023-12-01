"""***************************************************************************
File          : cli_test.py
About         : Test cli is working as expected 
Author        : Freddie Mercer
Date modified : 2023-12-01
***************************************************************************"""

import pytest
import src.cli as cli_obj

#-----------------------------------------------------------------------------
# Setup test enviro 
#-----------------------------------------------------------------------------

normal_pan = ['-p','123']
normal_rcode = ['-r','place']
normal = normal_pan + normal_rcode + ['-H']


class TestApi():

#-----------------------------------------------------------------------------
# 					     __init__ test 
# 	Function: initialise cli and parse the raw args 
# 	Tests: Need to make sure values parsed correctly, with correct error 
# 			handlings
#-----------------------------------------------------------------------------
	# Normal CLI
	def test_cli1_init(self):
		
		cli = cli_obj.cli_obj(normal)
		assert cli.args.human == True
	
	def test_cli2_init(self):
		pass