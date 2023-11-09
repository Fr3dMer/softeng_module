"""****************************************************************************
File          : PannelAppDB.py
About         : Hold main logical flow for app 
Author        : Freddie Mercer
****************************************************************************"""

import src.api as api_module
import src.cli as cli_module
import sys





def main():

    # CLI 
    cli = cli_module.cli_obj(sys.argv[1:])

    #print(cli.args.panel_id)
    
    # Instantiate api obj
    api = api_module.api_obj("args")
   
    # Check internet connection 
    internet_status = api.check_internet()

    # Call pannel from db, returning version 
    if(internet_status==True):
        # get panel_id from db  
        # For now parse json and get version 
        raw_data = api.get_single_detailed_pannel(cli.args.panel_id)
        query_version = parser.parser_version(raw_data)
        
    else:
        # No internet so get pannel_id from db and json data 
        raise SystemExit("Could not connect to internet")

    # Make a call to API and get GMS version 
    gms_panel = api.get_gms_pannel(cli.args.panel_id)
    gms_pannel_version = parsing.get_version(gms_pannel)

    # Compare versions
    if(api.version_check(gms_panel,query_version) == True):
        # If not changed, return version in db to variable 
        # Run parser and return each feature from data 
        pass
    else:
        # If GMS version has changed, get new version and push to db, return new version to variable
        # Call GMS pannel version 
         raw_data = api.get_single_detailed_pannel(cli.args.panel_id,gms_pannel_version)
         # Run parser and return each feature from data







if (__name__ == "__main__"):

   main()





