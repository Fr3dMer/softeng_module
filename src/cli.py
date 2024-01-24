"""***************************************************************************
File          : cli.py
About         : cli_obj
Author        : Freddie Mercer
****************************************************************************"""

import argparse


class cli_obj():
    
    def __init__(self,raw_args):
        
        parser = argparse.ArgumentParser(description = "An app for pulling NGS pannel data")
        
        parser.add_argument("-p",
                            "--panel_id",
                            type=int,
                            help="Panel identifier used by panelapp API")
        parser.add_argument("-r",
                            "--rcode",
                            type=str,
                            help="Search for pannel by rcode")
        parser.add_argument("-H",
                            "--human",
                            action="store_true",
                            help="View data in human readable format")
        
        self.args = parser.parse_args(raw_args)

        # Check if any panel id entered
        if (type(self.args.panel_id) == int or type(self.args.rcode == int)):
            self.return_panel_info = True
        else:
            self.return_panel_info = False

        # Check if any patient details enteres
        if (type(self.args.patientID) == str or type(self.args.sampletID) == str):
            self.patient_info == True
        else:
            self.patient_info == False



# - Need to add error catching for if patient ID suplied withought sample ID and vice versa
