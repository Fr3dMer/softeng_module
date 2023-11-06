#Import required modules
import json
import pandas as pd
import numpy as np

#Read json file
f = open('C:/Users/amy.grimwood/Downloads/JSON_eg_nodisease.json')

#Convert json object to df
data = json.load(f)


#Extract panel id from json, including error handelling for jsons missing the 'id' key

try:
    Panel_id = data['id']
except KeyError:
    print('KeyError:PanelApp output JSON doesn\' contain \'id\' key')
    Panel_id = np.nan

#Extract panel version from json, including error handelling for jsons missing the 'version' key
try:
    Panel_version = data['version']
except KeyError:
    print('KeyError:PanelApp output JSON doesn\' contain \'version\' key')
    Panel_version = np.nan

#Extract Disease from json, including error handelling for jsons missing the 'relevant_disorders' key
try:
    Disease = data['relevant_disorders']
except KeyError:
    print('KeyError:PanelApp output JSON doesn\' contain \'relevant_disorders\' key')
    Disease = np.nan

#Extract Date Last Updated from json, including error handelling for jsons missing the 'version_created' key
try:
    Last_updated = data['version_created']
    Last_updated = Last_updated[:Last_updated.index("T")]
except KeyError:
    print('KeyError:PanelApp output JSON doesn\' contain \'version_created\' key')
    Last_updated = np.nan

#Extract genes on panel from json, including error handelling for jsons mimissing the 'genes', 'gene_data' or 'hgnc_symbol' key>
try:
    gene_info = data['genes']
    gene_list = []
    for x in gene_info:
        genes = x.get('gene_data',{}).get('hgnc_symbol')
        gene_list.append(genes)
except KeyError:
    print('KeyError:PanelApp output JSON doesn\' contain \'genes\' or \'hgnc_symbol\' key')
    gene_list = np.nan

#Make df containing panel info
rows = ['Panel_id', 'Panel_version', 'Disease', 'Last_updated', 'Genes']

Values = [Panel_id, Panel_version, Disease, Last_updated, gene_list]

df = pd.DataFrame(Values, index =rows, columns=['Values'])
