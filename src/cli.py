"""***************************************************************************
File          : cli.py
About         : cli_obj
Author        : Freddie Mercer
****************************************************************************"""

import os
import argparse


class cli_obj():

    """ Obj for parsing and holding params passed in at start.

    Organisation:
    __init__(): Construct parser with appropriate arguments and
                then parse.
    check_args(): Error catching logic to prevent incompatable
                  combinations of arguments, check bed file paths
                  and generate general vars used in logic in main.
    """
    
    def __init__(self, raw_args):

        """Construct parser with appropriate arguments and 
        then parse.
        
        Keyword arguments:
            raw_args (list): takes output of sys.argv[1:]
        """

        # Construct parser
        app_des = "An app for pulling NGS pannel data"
        self.parser = argparse.ArgumentParser(description = app_des)
        self.parser.add_argument("-p",
                            "--panel_id",
                            type=int,
                            help="Panel identifier used by panelapp API")
        self.parser.add_argument("-r",
                            "--rcode",
                            type=str,
                            help="Search for pannel by rcode")
        self.parser.add_argument("-pid",
                            "--patientID",
                            type=str,
                            help="PatientID to insert into db")
        self.parser.add_argument("-sid",
                            "--sampleID",
                            type=str,
                            help="SampleID to insert into db")
        self.parser.add_argument("-g",
                            "--get_patient_data",
                            type=str,
                            help="Patient identifier to search for")
        self.parser.add_argument("-f",
                            "--fdb",
                            type=str,
                            help="DB location")
        self.parser.add_argument("-b37",
                            "--bed37",
                            type=str,
                            help="Location to save grch37 bed file")
        self.parser.add_argument("-b38",
                            "--bed38",
                            type=str,
                            help="Location to save grch38 bed file")
        self.parser.add_argument("-d",
                            "--debug_mode",
                            action="store_true",
                            help="Start script in debug mode")

        
        # Parse and save inside this obj
        self.args = self.parser.parse_args(raw_args)

        self.check_args()

    def check_args(self):

        """Error catching logic to prevent incompatable 
        combinations of arguments, check bed file paths 
        and generate general vars used in logic in main.
        """

        # Check sampleid and patientid supplied together 
        if len([x for x in (self.args.patientID,
                            self.args.sampleID) if x is not None]) == 1:
            error_msg = '--patientID and --sampleID must be given sampleID'
            self.parser.error(error_msg)

        # Check save location for bed37 exists
        if (type(self.args.bed37) == str):
            
            if (os.path.isfile(self.args.bed37)):
                error_msg = 'The path you provided for bed37 ' \
                            + 'does already exist'
                self.parser.error(error_msg)

        # Check save location for bed38 exists
        if (type(self.args.bed38) == str):
            
            if (os.path.isfile(self.args.bed38)):
                error_msg = 'The path you provided for bed38 ' \
                            + 'does already exist'
                self.parser.error(error_msg)

        # Check if any panel id entered
        if(self.args.panel_id == None and
           self.args.rcode == None):
            self.return_panel_info = False
        else:
            self.return_panel_info = True

        # Check if any patient details enteres
        if (type(self.args.patientID) == str):
            self.patient_info = True
        else:
            self.patient_info = False
