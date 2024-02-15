"""****************************************************************************
File          : JSON_parsing.py
About         : Parse information from PanelApp API to human readable text 
Author        : Freddie Mercer
****************************************************************************"""

"""This is the JSON_parsing module.
It parses data from the raw JSON returned from the pannel app API to extract 
pannel ID, pannel version, relevant disorders, date updated, genes included on
the pannel and collates the data into a JSON to be entered into the database.
"""

#Import required modules
import json
import pandas as pd
import numpy as np

class Parser():
    """Class extracts required data from Pannel app api outputs and recombines into JSON"""

    def __init__(self,args):
        self.args = args

    def extract_panel_id(self,input_json):
        """Extract panel id from json, including error handelling for jsons missing the 'id' key"""
        try:
            panel_id = input_json['id']
        except KeyError:
            print('KeyError:PanelApp output JSON doesn\' contain \'id\' key')
            panel_id = np.nan

        return panel_id

    def extract_version(self,input_json):
        """Extract panel version from json, including 
        error handelling for jsons missing the 'version' key
        """
        try:
            panel_version = input_json['version']
        except KeyError:
            print('KeyError:PanelApp output JSON doesn\' contain \'version\' key')
            panel_version = np.nan
        return panel_version

    def extract_disease(self,input_json):
        """Extract Disease from json, including error handelling for 
        jsons missing the 'relevant_disorders' key
        """
        try:
            disease = input_json['relevant_disorders']
        except KeyError:
            print('KeyError:PanelApp output JSON doesn\' contain \'relevant_disorders\' key')
            disease = np.nan
        return disease

    def extract_last_updated(self,input_json):
        """Extract Date Last Updated from json, including 
        error handelling for jsons missing the 'version_created' key
        """
        try:
            last_updated = input_json['version_created']
            last_updated = last_updated[:last_updated.index("T")]
        except KeyError:
            print('KeyError:PanelApp output JSON doesn\' contain \'version_created\' key')
            last_updated = np.nan
        return last_updated
    
    def extract_genes(self,input_json):
        """Extract genes on panel from json, including error 
        handelling for jsons mimissing the 'genes', 'gene_data' 
        or 'hgnc_symbol' key
        """
        try:
            gene_info = input_json['genes']
            gene_list = []
            for x in gene_info:
                #Given a key, the get() method returns paired value from
                #dict (documentation found at https://docs.python.org/2/library/stdtypes.html 
                #in section 5.8)
                hgnc_symbol = x.get('gene_data',{}).get('hgnc_symbol')
                hgnc_id = x.get('gene_data',{}).get('hgnc_id')
                GRch38_coord = (x.get('gene_data',{}).get('ensembl_genes',{})
                                .get('GRch38',{}).get('90',{}).get('location',{}))
                GRch37_coord = (x.get('gene_data',{}).get('ensembl_genes',{})
                                .get('GRch37',{}).get('82',{}).get('location',{}))
                gene_dict = {'HGNC Symbol':hgnc_symbol, 'HGNC ID':hgnc_id, 'GRch38 location':GRch38_coord}
                gene_list.append(gene_dict)
        except KeyError:
            print('KeyError:PanelApp output JSON doesn\' contain \'genes\' or an associated sub-key')
            gene_list = np.nan
        return gene_list

    def generate_bed(self,input_json,ref_seq='grch38'):
        """Generate BED file text, including error handelling 
        for jsons mimissing the 'genes' or 'location' key
        """
        try:
            gene_info = input_json['genes']
            location_list = []
            for x in gene_info:
                if ref_seq == 'grch38':
                    location = ('chr'+x.get('gene_data',{}).get('ensembl_genes',{})
                                .get('GRch38',{}).get('90',{}).get('location',{}))
                if ref_seq == 'grch37':
                    location = ('chr'+x.get('gene_data',{}).get('ensembl_genes',{})
                                .get('GRch37',{}).get('82',{}).get('location',{}))
                else: 
                    pass
                bed_str = np.nan
                location_list.append(location)
            location_str = "\n".join(location_list)
            bed_str = location_str.replace(':',' ').replace('-',' ')
        except KeyError:
            print('KeyError:PanelApp output JSON doesn\'t contain \'genes\' or \'location\' key')
            bed_str = np.nan
        return bed_str

