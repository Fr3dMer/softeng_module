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

normal_pan = ['-p',
			  '123']
normal_rcode = ['-r',
				'place']
normal = normal_pan + normal_rcode + ['-H']
no_panelid = ['-p'] + normal_rcode
no_rcode = normal_pan + ['-r']


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
		assert cli.args.panel_id == int(normal_pan[1])
		assert cli.args.rcode == normal_rcode[1]
		assert cli.args.human == True
	

	# Neither value present returns  error 
	def test_cli2_init(self):
		
		with pytest.raises(SystemExit):
			cli_obj.cli_obj(no_panelid)
		
		with pytest.raises(SystemExit):
			cli_obj.cli_obj(no_rcode)


	# Finally test Human bool flag 
	def test_cli2_init(self):

		cli = cli_obj.cli_obj(normal[0:-1])
		assert cli.args.human == False

