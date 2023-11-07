"""****************************************************************************
File          : api.py
About         : Object for interacting with pannelapp api 
Author        : Freddie Mercer
****************************************************************************"""

import requests


# Needs logic for checking version of pannel is most up to date 


# Check which pannel is up to date 
# Collect all pannel versions
# Collect pannel data based on version 
# Collect detailed pannel data for provided pannel 
class api_obj():


    def __init__(self,args):
        self.args = args

        url = "https://panelapp.genomicsengland.co.uk/api/v1/panels/3/?version=4.0"


    def get_all_pannels(self):

        url = "https://panelapp.genomicsengland.co.uk/api/v1/panels/signedoff/"

        return requests.get(url)

    def get_single_detailed_pannel(self,pannel_id,version):

        if(type(version) == int):
            print("incorrect value type for version provided, please use a string or float")
            raise SystemError

        url = "https://panelapp.genomicsengland.co.uk/api/v1/panels/3/"       
        payload = {'version':version} 

        return requests.get(url,params=payload)

    def value_checker(self,pannel_id,version):

        if(type(version) == int):
            print("incorrect value type for version provided, please use a string or float")
            raise SystemError
        
        if(type(pannel_id) == int):
            print("incorrect value type for version provided, please use a string or float")
            raise SystemError




if (__name__ == "__main__"):
    api = api_obj("arg")

    result = api.get_single_detailed_pannel(3,4)

    print(result.json())




