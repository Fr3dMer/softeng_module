
import json
import pandas as pd
import numpy as np

class Parser():


    def __init__(self,args):
        self.args = args

    def extract_panel_id(self,input_json):

        try:
            panel_id = input_json['id']
        except KeyError:
            print('KeyError:PanelApp output JSON doesn\' contain \'id\' key')
            panel_id = np.nan

        return panel_id

    def extract_version(self,input_json):
        try:
            panel_version = input_json['version']
        except KeyError:
            print('KeyError:PanelApp output JSON doesn\' contain \'version\' key')
            panel_version = np.nan
        return panel_version

    def extract_disease(self,input_json):
        try:
            disease = input_json['relevant_disorders']
        except KeyError:
            print('KeyError:PanelApp output JSON doesn\' contain \'relevant_disorders\' key')
            disease = np.nan
        return disease

    def extract_last_updated(self,input_json):
        try:
            last_updated = input_json['version_created']
            last_updated = last_updated[:last_updated.index("T")]
        except KeyError:
            print('KeyError:PanelApp output JSON doesn\' contain \'version_created\' key')
            last_updated = np.nan
        return last_updated
    
    def extract_genes(self,input_json):
        try:
            gene_info = input_json['genes']
            gene_list = []
            for x in gene_info:
                genes = x.get('gene_data',{}).get('hgnc_id')
                gene_list.append(genes)
        except KeyError:
            print('KeyError:PanelApp output JSON doesn\' contain \'genes\' or \'hgnc_id\' key')
            gene_list = np.nan
        return gene_list

