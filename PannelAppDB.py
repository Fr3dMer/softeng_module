"""****************************************************************************
File          : PannelAppDB.py
About         : Hold main logical flow for app 
Author        : Freddie Mercer
****************************************************************************"""

import sys
import src.api as api_module
import src.cli as cli_module
import src.JSON_parsing as parser_obj

def main():

    # Initiaslise CLI obj
    cli = cli_module.cli_obj(sys.argv[1:])
    
    # Instantiate api obj, parser and DB
    api = api_module.api_obj("args")
    parser = parser_obj.Parser("args")

    # Check internet connection
    internet_status = api.check_internet()

    # If no internet, get panel from db
    if not(internet_status==True):
        raise SystemExit("Could not connect to internet")
    
    # Otherwise using panel id, get most recent GMS panel
    elif(type(cli.args.panel_id) == int):
        raw_data = api.get_single_detailed_pannel_id(cli.args.panel_id)
        raw_data = api.get_gms_versions(raw_data,parser,api)

    # If no panel id, get most recent gms panel using R-code
    elif(type(cli.args.rcode) == str):
        raw_data = api.get_single_detailed_pannel_rcode(cli.args.rcode)
        raw_data = api.get_gms_versions(raw_data,parser,api)
    
    else:
        raise SystemExit("Panel id or Rcode must be entered")

    # Re parse all data again
    used_version = raw_data.get("version",None)
    disease = parser.extract_disease(raw_data)
    updated = parser.extract_last_updated(raw_data)
    genes = parser.extract_genes(raw_data)

    # Send parsed data to db

    # Print all parsed data
    print("Panel id :          ",query_id)
    print("Version :           ",used_version)
    print("Disease:            ",disease[0])
    print("Last updated:       ",updated)
    print("Genes in list:      ",genes)

    






if (__name__ == "__main__"):

   main()





