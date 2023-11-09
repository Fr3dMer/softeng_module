"""****************************************************************************
File          : PannelAppDB.py
About         : Hold main logical flow for app 
Author        : Freddie Mercer
****************************************************************************"""

import src.api as api_module
import src.cli as cli_module
import src.JSON_parsing as parser_obj
import sys





def main():

    # CLI 
    cli = cli_module.cli_obj(sys.argv[1:])
    
    # Instantiate api obj and parser
    api = api_module.api_obj("args")
    parser = parser_obj.Parser("args")
   


    # Check internet connection 
    internet_status = api.check_internet()

    # Call pannel from db, returning version 
    if(internet_status==True):
        # get panel_id from db  
        # For now parse json and get version 
        raw_data = api.get_single_detailed_pannel(cli.args.panel_id)
        query_version = float(parser.extract_version(raw_data))
        
    else:
        # No internet so get pannel_id from db and json data 
        raise SystemExit("Could not connect to internet")

    # Make a call to API and get GMS version 
    gms_panel = api.get_gms_pannel(cli.args.panel_id)
    gms_pannel_version = float(gms_panel.get("version",None))



    # Compare versions
    if(api.version_check(gms_pannel_version,query_version) == True):
        # If not changed, return version in db to variable 
        # Run parser and return each feature from data 
        pass
    else:
        # If GMS version has changed, get new version and push to db, return new version to variable
        # Call GMS pannel version 
        raw_data = api.get_single_detailed_pannel(cli.args.panel_id,gms_pannel_version)
        # Run parser and return each feature from data


    id = parser.extract_panel_id(raw_data)    
    disease = parser.extract_disease(raw_data)
    updated = parser.extract_last_updated(raw_data)
    genes = parser.extract_genes(raw_data)

    print("Panel id : ",id,"\n")
    print("Disease: ",disease,"\n")
    print("Last updated: ",updated,"\n")
    print("Genes in list: ",genes,"\n")

    






if (__name__ == "__main__"):

   main()





