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

    cli = cli_module.cli_obj(sys.argv[1:])
    
    api = api_module.api_obj("args")
    parser = parser_obj.Parser("args")

    internet_status = api.check_internet()

    if not(internet_status==True):
        raise SystemExit("Could not connect to internet")
        
    if(type(cli.args.panel_id) == int):
        raw_data = api.get_single_detailed_pannel_id(cli.args.panel_id)

    elif(type(cli.args.rcode) == str):
        raw_data = api.get_single_detailed_pannel_rcode(cli.args.rcode)

    query_version = float(parser.extract_version(raw_data))
    query_id = int(parser.extract_panel_id(raw_data))
    gms_panel = api.get_gms_pannel(query_id)
    gms_pannel_version = float(gms_panel.get("version",None))

    if(api.version_check(gms_pannel_version,query_version) == False):
        raw_data = api.get_single_detailed_pannel_id(query_id,gms_pannel_version)


    used_version = raw_data.get("version",None)
    disease = parser.extract_disease(raw_data)
    updated = parser.extract_last_updated(raw_data)
    genes = parser.extract_genes(raw_data)

    print("Panel id :          ",query_id)
    print("Version :           ",used_version)
    print("Disease:            ",disease[0])
    print("Last updated:       ",updated)
    print("Genes in list:      ",genes)

    






if (__name__ == "__main__"):

   main()





