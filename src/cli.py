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

