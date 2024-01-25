"""****************************************************************************
File          : PannelAppDB.py
About         : Hold main logical flow for app 
Author        : Freddie Mercer
****************************************************************************"""




import pandas as pd
import src.api as api_module
import src.cli as cli_module
import src.JSON_parsing as parser_obj
import src.logging_1_0 as log_obj
import sys
#import src.database_3_0.py as db
from datetime import datetime

def main():

    # Initiaslise CLI obj
    cli = cli_module.cli_obj(sys.argv[1:])
    
    # Instantiate logger, api obj, parser and DB
    logger = log_obj.LoggerManager()
    api = api_module.api_obj(logger)
    parser = parser_obj.Parser("args")

    # Check internet connection
    internet_status = api.check_internet()
    int_disc = "#######################################################\n" \
               + "Can't connect to internet, returning panel saved in db"  \
               + "#######################################################\n"

    # If no internet, get panel from db using rcode
    if(internet_status == False and type(cli.args.rcode) == str):
        #raw_data = db.retrieve_highest_version_json(cli.args.rcode)
        print(int_disc)
    
    # If no internet, get panel from db using ponel id
    elif(internet_status == False and type(cli.panel_id.rcode) == int):
        #raw_data = db.retrieve_highest_version_json(cli.panel_id.rcode)
        print(int_disc)

    # Otherwise using panel id, get most recent GMS panel
    elif(type(cli.args.panel_id) == int):
        raw_data = api.get_single_detailed_pannel_id(cli.args.panel_id)
        raw_data = api.get_gms_versions(raw_data,parser)

    # If no panel id, get most recent gms panel using R-code
    elif(type(cli.args.rcode) == str):
        raw_data = api.get_single_detailed_pannel_rcode(cli.args.rcode)
        raw_data = api.get_gms_versions(raw_data,parser)
    
    else:
        raise SystemExit("Panel id or Rcode must be entered")

    # Check None has been returned, which is returned by 
    # db retrieve_highest_version_json if panel not present in db 
    if (raw_data == None):
        raise SystemExit("No GMS panels present in database")

    #print(cli.return_panel_info)
    if (cli.return_panel_info == True):

        # Re parse all data again
        query_id = int(parser.extract_panel_id(raw_data))
        used_version = raw_data.get("version",None)
        r_code = parser.extract_disease(raw_data)[0]
        updated = parser.extract_last_updated(raw_data)
        genes = parser.extract_genes(raw_data)
        BED_GrCH37 = parser.generate_bed(raw_data)
        ############## TODO: MAKE SURE GRCH38 BEING CREATED, THIS IS PLACE HOLDER!!!! #####################
        BED_GrCH38 = parser.generate_bed(raw_data)

        # Send parsed data to db
        unique_panel_id = r_code + "-" + used_version
        #db.insert_panel_record(unique_panel_id, 
        #                    r_code, 
        #                    used_version, 
         #                   genes, 
          #                  raw_data, 
           #                 BED_GrCH37, 
            #                BED_GrCH38)

        # Print all parsed data
        print("Panel id :          ",query_id)
        print("Version :           ",used_version)
        print("Disease:            ",r_code)
        print("Last updated:       ",updated)
        # Create table 
        output = pd.DataFrame(data=genes)
        print(output.to_markdown())

    # Send patient data to db 
    if(cli.patient_info == True):

        today_date = datetime.now()
        #db.insert_patient_record(cli.args.patientID,
         #                        cli.args.sampleID,
          #                       unique_panel_id,
           #                      today_date)    



    # Get patient data if option present
    #if(type(cli.get_patient_data) == str):
    #    #pat_data = db.retrieve_patient_and_panel_info(cli.get_patient_data)
    #    #print(pat_data)
    #    pass
    


if (__name__ == "__main__"):

   main()