"""***************************************************************************
File          : cli.py
About         : cli_obj
Author        : Freddie Mercer
****************************************************************************"""

import argparse


class cli_obj():

    """ Obj for parsing and holding params passed in at start.
    Organisation:
    __init__(): Construct parser with appropriate arguments and 
                then parse.
    check_patient(): Error catching logic to prevent incompatable 
                     combinations of arguments.
    """
    
    def __init__(self,raw_args):

        """Construct parser with appropriate arguments and 
        then parse.
        
        Keyword arguments:
        raw_args (list): output of sys.argv[1:]
        """
        
        parser = argparse.ArgumentParser(description = "An app for pulling NGS pannel data")
        
        parser.add_argument("-p",
                            "--panel_id",
                            type=int,
                            help="Panel identifier used by panelapp API")
        parser.add_argument("-r",
                            "--rcode",
                            type=str,
                            help="Search for pannel by rcode")
        parser.add_argument("-pid",
                            "--patientID",
                            type=str,
                            help="PatientID to insert into db")
        parser.add_argument("-sid",
                            "--sampleID",
                            type=str,
                            help="SampleID to insert into db")
        
        self.args = parser.parse_args(raw_args)

        # Check if any panel id entered
        if (type(self.args.panel_id) == int or type(self.args.rcode == int)):
            self.return_panel_info = True
        else:
            self.return_panel_info = False

        # Check if any patient details enteres
        if (type(self.args.patientID) == str or type(self.args.sampleID) == str):
            self.patient_info == True
        else:
            self.patient_info == False

    def check_patient(self):

        """Error catching logic to prevent incompatable 
        combinations of arguments.
        
        Keyword arguments:
        None needed

        Returns:
        Bool: True if issues, False if no incompatabilities
        """


# - Need to add error catching for if patient ID suplied withought sample ID and vice versa
