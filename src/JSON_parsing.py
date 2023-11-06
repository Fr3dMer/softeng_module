#Import required modules
import json
import pandas as pd
import numpy as np

# Object to parse JSON output from app.py 
class Parser():

    # Constructor 
    def __init__(self,args):
        self.args = args

    
    #Read json file
    #f = open('/home/amy/git/softeng_module/src/JSON_eg.json')


    #Convert json file to dict
    #data = json.load(f)

    #Extract panel id from json, including error handelling for jsons missing the 'id' key
    def extract_panel_id(self,input_json):

        try:
            panel_id = input_json['id']
        except KeyError:
            print('KeyError:PanelApp output JSON doesn\' contain \'id\' key')
            panel_id = np.nan

        return panel_id
    
    #Extract panel version from json, including error handelling for jsons missing the 'version' key
    def extract_version(self,input_json):
        try:
            panel_version = input_json['version']
        except KeyError:
            print('KeyError:PanelApp output JSON doesn\' contain \'version\' key')
            panel_version = np.nan
        return panel_version
    
     #Extract Disease from json, including error handelling for jsons missing the 'relevant_disorders' key
    def extract_disease(self,input_json):
        try:
            disease = input_json['relevant_disorders']
        except KeyError:
            print('KeyError:PanelApp output JSON doesn\' contain \'relevant_disorders\' key')
            disease = np.nan
        return disease

    #Extract Date Last Updated from json, including error handelling for jsons missing the 'version_created' key
    def extract_last_updated(self,input_json):
        try:
            last_updated = input_json['version_created']
            last_updated = last_updated[:last_updated.index("T")]
        except KeyError:
            print('KeyError:PanelApp output JSON doesn\' contain \'version_created\' key')
            last_updated = np.nan
        return last_updated
    
    #Extract genes on panel from json, including error handelling for jsons mimissing the 'genes', 'gene_data' or 'hgnc_symbol' key>
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

        
        #Make df containing panel info
        #rows = ['Panel_id', 'Panel_version', 'Disease', 'Last_updated', 'Genes']

        #Values = [Panel_id, Panel_version, Disease, Last_updated, gene_list]

        #df = pd.DataFrame(Values, index =rows, columns=['Values'])

        #print(df)
