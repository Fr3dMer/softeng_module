"""****************************************************************************
File          : api.py
About         : Object for interacting with pannelapp api 
Author        : Freddie Mercer
****************************************************************************"""

import requests


# Object to make call to gel pannel app rest api
class api_obj():

    # Constructor 
    def __init__(self,args):
        self.args = args

        url = "https://panelapp.genomicsengland.co.uk/api/v1/panels/3/?version=4.0"

    # Call endpoint to get most up to date version of signed off pannel 
    def get_all_pannels(self,pannel_id):

        self.value_checker(pannel_id=pannel_id)

        url = "https://panelapp.genomicsengland.co.uk/api/v1/panels/signedoff/"
        payload = {'panel_id':pannel_id} 

        return requests.get(url,params=payload)

    # Get detailed info on individual pannel
    def get_single_detailed_pannel(self,pannel_id,version):

        self.value_checker(version=version,pannel_id=pannel_id)

        url = "https://panelapp.genomicsengland.co.uk/api/v1/panels/" + str(pannel_id) + "/"       
        payload = {'version':version} 

        return requests.get(url,params=payload)

    # Support func to ensure variables in correct format 
    def value_checker(self,pannel_id,version=""):

        if(type(version) == int):
            print("incorrect value type for version provided, please use a string or float")
            raise SystemError
        
        if(type(pannel_id) != int):
            print("incorrect value type for version provided, please use a string or float")
            raise SystemError
        
    # Compare version and 
    #def 




if (__name__ == "__main__"):
    api = api_obj("arg")

    result = api.get_single_detailed_pannel(3,4.0)
    result2 = api.get_all_pannels(3)

    print(result.json(),"\n\n")
    print(result2.json())




