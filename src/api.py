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

    # Call endpoint to get most up to date version of signed off pannel 
    def get_gms_pannel(self,pannel_id):

        self.value_checker(pannel_id=pannel_id)

        url = "https://panelapp.genomicsengland.co.uk/api/v1/panels/signedoff/"+ str(pannel_id)

        return requests.get(url).json()

    # Get detailed info on individual pannel via id
    def get_single_detailed_pannel_id(self,pannel_id,version=None):
        
        if(version==None):
            url = "https://panelapp.genomicsengland.co.uk/api/v1/panels/" + str(pannel_id) 
            return requests.get(url).json()

        self.value_checker(version=version,pannel_id=pannel_id)

        url = "https://panelapp.genomicsengland.co.uk/api/v1/panels/" + str(pannel_id) + "/"       
        payload = {'version':version} 

        return requests.get(url,params=payload).json()

    # Get detailed info on individual pannel via rcode
    def get_single_detailed_pannel_rcode(self,rcode,version=None):
        
        self.value_checker(version=version,rcode=rcode)

        url = "https://panelapp.genomicsengland.co.uk/api/v1/panels/" + str(rcode) 
        return requests.get(url).json()



    # Support func to ensure variables in correct format 
    def value_checker(self,pannel_id=None,version=None,rcode=None):


        if not(version == None or type(version) == float or type(version) == str):
            raise SystemError("Internal error: incorrect value type for version used for api cal, please use a string or float")
      
        if not(pannel_id == None or type(pannel_id) == int):
            raise SystemError("Internal error: incorrect value type for panel id used for api call, please use a int")
        
        if not(rcode == None or type(rcode) == str):
            raise SystemError("Internal error: incorrect value type for rcode used for api call, please provide a str")
    
    def version_check(self,query_version,true_version):
        
        # Make sure versions are correct type 
        if not (type(query_version) == float and type(true_version) == float):
            raise SyntaxError("Verions are not floats, cannot compare versions")

        # If versions are equal 
        if(query_version == true_version):            
            
            return True

        # 2.3 > 5 == True
        elif(query_version != true_version):
            return False
        
    # Check internet connection 
    def check_internet(self):
        url = 'http://google.com'

        try:
            response = requests.get(url, timeout=5)
        except:
            return False
        else:
            return True







if (__name__ == "__main__"):

    api = api_obj("arg")


    result = api.get_single_detailed_pannel(pannel_id=3,version=4.0)
    result2 = api.get_gms_pannel(3)

    print(result,"\n\n")
    print(result2)




