"""****************************************************************************
File          : PannelAppDB.py
About         : Hold main logical flow for app 
Author        : Freddie Mercer
****************************************************************************"""

import sys
import json
import pandas as pd
import src.api as api_module
import src.cli as cli_module
import src.logging as log_obj
from datetime import datetime
import src.database_3_0 as db_obj
import src.JSON_parsing as parser_obj


def main():
    """Main function for script, tying together logic and objects 
    in one place"""
    
    # Initiaslise CLI obj
    cli = cli_module.cli_obj(sys.argv[1:])

    # Init logger
    log = log_obj.LoggerManager(debug_mode=cli.args.debug_mode)
    log.logger.debug("Initialising objects")
    
    # Instantiate api obj, parser and DB
    api = api_module.api_obj(log)
    parser = parser_obj.Parser("args")
    # See if db url has been added 
    if(type(cli.args.fdb) == str):
        db_url = 'sqlite:///' + cli.args.fdb + 'panel_app_db.db'
        db_folder = cli.args.fdb
    else:
        db_url = 'sqlite:///panel_app_db.db'
        db_folder = ""
    log.logger.debug("Connecting to DB")
    db = db_obj.PanelAppDB(db_url)

    # Check internet connection
    internet_status = api.check_internet()
    int_disc = "#######################################################\n" \
               + "Can't connect to internet, returning panel saved in db"  \
               + "#######################################################\n"

    # If no internet, get panel from db using rcode
    raw_data = ""
    if(internet_status == False and type(cli.args.rcode) == str):
        raw_data = db.retrieve_highest_version_json(cli.args.rcode)
        log.logger.warning(int_disc)
    
    # If no internet, get panel from db using panel id
    elif(internet_status == False and type(cli.panel_id.rcode) == int):
        raw_data = db.retrieve_highest_version_json(cli.panel_id.rcode)
        log.logger.warning(int_disc)

    # Otherwise using panel id, get most recent GMS panel
    elif(type(cli.args.panel_id) == int):
        raw_data = api.get_single_detailed_pannel_id(cli.args.panel_id)
        raw_data = api.get_gms_versions(raw_data,parser)

    # If no panel id, get most recent gms panel using R-code
    elif(type(cli.args.rcode) == str):
        raw_data = api.get_single_detailed_pannel_rcode(cli.args.rcode)
        raw_data = api.get_gms_versions(raw_data,parser)
    

    # Check None has been returned, which is returned by 
    # db retrieve_highest_version_json if panel not present in db 
    if (raw_data == None):
        log.logger.error("No GMS panels present in database")
        raise SystemExit

    #print(cli.return_panel_info)
    if (cli.return_panel_info == True):
        log.logger.debug("Parsing data")

        # Re parse all data again
        query_id = int(parser.extract_panel_id(raw_data))
        used_version = raw_data.get("version",None)
        r_code = parser.extract_disease(raw_data)[0]
        updated = parser.extract_last_updated(raw_data)
        genes = parser.extract_genes(raw_data)
        BED_GrCH37 = parser.generate_bed(raw_data,'grch38')
        BED_GrCH38 = parser.generate_bed(raw_data,'grch37')
        unique_panel_id = r_code + "-" + used_version + "-" + str(query_id)

        log.logger.debug("Generating bed files")

        # Save beds
        if(type(cli.args.bed37) == str):
            bed37_name = cli.args.bed37
        else:
            bed37_name = db_folder + unique_panel_id + "-bed37.bed"
        
        if(type(cli.args.bed38) == str):
            bed38_name = cli.args.bed38
        else:
            bed38_name = db_folder + unique_panel_id + "-bed38.bed"

        with open(bed37_name, 'w') as file:
            file.write(BED_GrCH37)

        with open(bed38_name, 'w') as file:
            file.write(BED_GrCH38)
        
        # Send parsed data to db
        log.logger.debug("Inserting GMS panel data into db")
        db.insert_panel_record_panelid(unique_panel_id, 
                            query_id,
                            r_code, 
                            used_version, 
                            str(genes),
                            json.dumps(raw_data, indent=2).encode('utf-8'),
                            BED_GrCH37, 
                            BED_GrCH38)
        db.connection.commit()
        
        log.logger.debug("Printing panel details")
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
        log.logger.debug("Inserting patient details")
        today_date = datetime.now()
        db.insert_patient_record(cli.args.patientID,
                                 cli.args.sampleID,
                                 unique_panel_id,
                                 today_date)    
        db.connection.commit()



    # Get patient data if option present
    if(type(cli.args.get_patient_data) == str):
        log.logger.debug("Getting patient details")
        pat_data = db.retrieve_patient_and_panel_info(
                            cli.args.get_patient_data)
        for item in pat_data:
            #pat_list = [item[0],item[1],item[2],item[3],item[4],item[5]]
            formatted_date = (str(item[2].day)+'/'+str(item[2].month)+
                              '/'+str(item[2].year)+' '+str(item[2].hour)+':'+str(item[2].minute))
            pat_dict = {'Sample ID: ':item[0],'Patient ID: ':item[1], 'Date: ':formatted_date,
                        'PanelApp ID: ':item[3],'Rcode: ':item[4],'Version: ':item[5]}
            print("Returned patient records:",pat_dict)

    # Close db connection
    db.connection.close()


if (__name__ == "__main__"):

    main()
