"""***************************************************************************
File          : JSON_parsing.py
About         : Ensure JSON are parsed as expected 
Author        : Freddie Mercer
Date modified : 2023-12-01

TODO: Need to capture logs once logging implemented
***************************************************************************"""

import json
import pytest
import numpy as np
import src.JSON_parsing as JSON_obj

#-----------------------------------------------------------------------------
# Setup test enviro 
#-----------------------------------------------------------------------------

empty_json = {"":"","":""}

@pytest.fixture
def normal_json():
    f = open("test/JSON_test_data.json")
    normal_json = json.load(f)
    f.close
    yield normal_json

@pytest.fixture
def json_obj():
    yield JSON_obj.Parser("args")

gene_list = [{'HGNC Symbol': 'APC', 
              'HGNC ID': 'HGNC:583', 
              'GRch38 location': '5:112707498-112846239'}, 
             {'HGNC Symbol': 'BMPR1A', 
              'HGNC ID': 'HGNC:1076', 
              'GRch38 location': '10:86756601-86932838'}, 
             {'HGNC Symbol': 'EPCAM', 
              'HGNC ID': 'HGNC:11529', 
              'GRch38 location': '2:47345158-47387601'}, 
             {'HGNC Symbol': 'MLH1', 
              'HGNC ID': 'HGNC:7127', 
              'GRch38 location': '3:36993332-37050918'}, 
             {'HGNC Symbol': 'MSH2', 
              'HGNC ID': 'HGNC:7325', 
              'GRch38 location': '2:47402969-47562311'}, 
             {'HGNC Symbol': 'MSH6', 
              'HGNC ID': 'HGNC:7329', 
              'GRch38 location': '2:47695530-47810101'}, 
             {'HGNC Symbol': 'MUTYH', 
              'HGNC ID': 'HGNC:7527', 
              'GRch38 location': '1:45329163-45340470'}, 
             {'HGNC Symbol': 'NTHL1', 
              'HGNC ID': 'HGNC:8028', 
              'GRch38 location': '16:2039815-2047866'}, 
             {'HGNC Symbol': 'PMS2', 
              'HGNC ID': 'HGNC:9122', 
              'GRch38 location': '7:5973239-6009125'}, 
             {'HGNC Symbol': 'POLD1', 
              'HGNC ID': 'HGNC:9175', 
              'GRch38 location': '19:50384204-50418018'}, 
             {'HGNC Symbol': 'POLE', 
              'HGNC ID': 'HGNC:9177', 
              'GRch38 location': '12:132623753-132687365'}, 
             {'HGNC Symbol': 'PTEN', 
              'HGNC ID': 'HGNC:9588', 
              'GRch38 location': '10:87863113-87971930'}, 
             {'HGNC Symbol': 'RNF43', 
              'HGNC ID': 'HGNC:18505', 
              'GRch38 location': '17:58352500-58417595'}, 
             {'HGNC Symbol': 'SMAD4', 
              'HGNC ID': 'HGNC:6770', 
              'GRch38 location': '18:51028394-51085045'}, 
             {'HGNC Symbol': 'STK11', 
              'HGNC ID': 'HGNC:11389', 
              'GRch38 location': '19:1177558-1228435'}, 
             {'HGNC Symbol': 'AXIN2', 
              'HGNC ID': 'HGNC:904', 
              'GRch38 location': '17:65528563-65561647'}, 
             {'HGNC Symbol': 'GREM1', 
              'HGNC ID': 'HGNC:2001', 
              'GRch38 location': '15:32717974-32745107'}, 
             {'HGNC Symbol': 'MBD4', 
              'HGNC ID': 'HGNC:6919', 
              'GRch38 location': '3:129430944-129440179'}, 
             {'HGNC Symbol': 'MSH3', 
              'HGNC ID': 'HGNC:7326', 
              'GRch38 location': '5:80654648-80876460'}] 

bed_str = "chr5 112707498 112846239\n" + \
          "chr10 86756601 86932838\n" + \
          "chr2 47345158 47387601\n" + \
          "chr3 36993332 37050918\n" + \
          "chr2 47402969 47562311\n" + \
          "chr2 47695530 47810101\n" + \
          "chr1 45329163 45340470\n" + \
          "chr16 2039815 2047866\n" + \
          "chr7 5973239 6009125\n" + \
          "chr19 50384204 50418018\n" + \
          "chr12 132623753 132687365\n" + \
          "chr10 87863113 87971930\n" + \
          "chr17 58352500 58417595\n" + \
          "chr18 51028394 51085045\n" + \
          "chr19 1177558 1228435\n" + \
          "chr17 65528563 65561647\n" + \
          "chr15 32717974 32745107\n" + \
          "chr3 129430944 129440179\n" + \
          "chr5 80654648 80876460"


class TestJSON_parsing():

#-----------------------------------------------------------------------------
# 					     extract_panel_id test 
# 	Function: extract pannel id from JSON
# 	Tests: Can it deal with normal JSON and when its not present?
#-----------------------------------------------------------------------------
    def test_json1_extract_panel_id (self,json_obj,normal_json):

        # Normal
        assert json_obj.extract_panel_id(normal_json) == 504

        # Does it raise errors as expected?
        assert np.isnan(json_obj.extract_panel_id(empty_json)) == True


#-----------------------------------------------------------------------------
# 					     extract_version test 
# 	Function: extract version from json
# 	Tests: Can it deal with normal JSON and when its not present?
#-----------------------------------------------------------------------------
    def test_json2_extract_panel_id(self,json_obj,normal_json):

        # Normal
        assert json_obj.extract_version(normal_json) == '2.8'

        # Does it raise errors as expected?
        assert np.isnan(json_obj.extract_version(empty_json)) == True


#-----------------------------------------------------------------------------
# 					     extract_disease test 
# 	Function: extract associated dieases with test
# 	Tests: Can it deal with normal JSON and when its not present?
#-----------------------------------------------------------------------------
    def test_json3_extract_disease(self,json_obj,normal_json):

        # Normal
        assert json_obj.extract_disease(normal_json) == ['Inherited ' + \
                                                         'polyposis', 
                                                         'R211']

        # Does it raise errors as expected?
        assert np.isnan(json_obj.extract_disease(empty_json)) == True


#-----------------------------------------------------------------------------
#                        extract_last_updated test 
#   Function: extract date the panel was last updated
#   Tests: Can it deal with normal JSON and when its not present?
#-----------------------------------------------------------------------------
    def test_json3_extract_last_updated(self,json_obj,normal_json):

        # Normal
        assert json_obj.extract_last_updated(normal_json) == '2023-10-26'

        # Does it raise errors as expected?
        assert np.isnan(json_obj.extract_last_updated(empty_json)) == True


#-----------------------------------------------------------------------------
#                        extract_genes test 
#   Function: extract genes present and return as a list
#   Tests: Can it deal with normal JSON and when its not present?
#-----------------------------------------------------------------------------
    def test_json4_extract_genes(self,json_obj,normal_json):

        # Normal
        assert json_obj.extract_genes(normal_json) == gene_list

        # Does it raise errors as expected?
        assert np.isnan(json_obj.extract_genes(empty_json)) == True


#-----------------------------------------------------------------------------
#                        generate_bed test 
#   Function: generate bed using infor from json
#   Tests: Can it deal with key error, normal data 
#-----------------------------------------------------------------------------
    def test_json4_generate_bed(self,json_obj,normal_json):

        # Normal
        assert json_obj.generate_bed(normal_json) == bed_str

        # blank
        assert np.isnan(json_obj.generate_bed(empty_json)) == True
