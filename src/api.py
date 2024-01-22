"""****************************************************************************
File          : api.py
About         : Object for interacting with pannelapp api 
Author        : Freddie Mercer
Date modified : 2023-12-08
****************************************************************************"""

import requests


class api_obj():


    def __init__(self,args):
        self.args = args

    def get_gms_pannel(self,pannel_id):

        self.value_checker(pannel_id=pannel_id)

        url = "https://panelapp.genomicsengland.co.uk/api/v1/panels/signedoff/"+ str(pannel_id)

        return requests.get(url).json()

    def get_single_detailed_pannel_id(self,pannel_id,version=None):
        
        if(version==None):
            url = "https://panelapp.genomicsengland.co.uk/api/v1/panels/" + str(pannel_id) 
            return requests.get(url).json()

        self.value_checker(version=version,pannel_id=pannel_id)

        url = "https://panelapp.genomicsengland.co.uk/api/v1/panels/" + str(pannel_id) + "/"       
        payload = {'version':version} 

        return requests.get(url,params=payload).json()

    def get_single_detailed_pannel_rcode(self,rcode,version=None):
        
        self.value_checker(version=version,rcode=rcode)

        url = "https://panelapp.genomicsengland.co.uk/api/v1/panels/" + str(rcode) 
        return requests.get(url).json()


    def value_checker(self,pannel_id=None,version=None,rcode=None):

        if not(version == None or type(version) == float or type(version) == str):
            raise SystemError("Internal error: incorrect value type for version used for api cal, please use a string or float")
      
        if not(pannel_id == None or type(pannel_id) == int):
            raise SystemError("Internal error: incorrect value type for panel id used for api call, please use a int")
        
        if not(rcode == None or type(rcode) == str):
            raise SystemError("Internal error: incorrect value type for rcode used for api call, please provide a str")
    
    def version_check(self,query_version,true_version):

        if not (type(query_version) == float and type(true_version) == float):
            raise SyntaxError("Versions are not floats, cannot compare versions")

        if(query_version == true_version):            
            
            return True

        elif(query_version != true_version):
            return False

    def check_internet(self,url = 'http://google.com'):
        
        try:
            response = requests.get(url, timeout=5)
        except:
            return False
        else:
            return True

    # Extracts version from raw_data, calls api to ensure most recent GMS panel, 
    # if not gets most recent GMS panel
    def get_gms_versions(self,raw_data,parser):

        # Make a call to API and get GMS version
        query_version = float(parser.extract_version(raw_data))
        query_id = int(parser.extract_panel_id(raw_data))
        gms_panel = self.get_gms_pannel(query_id)
        gms_pannel_version = float(gms_panel.get("version",None))

        # Compare versions
        if(self.version_check(gms_pannel_version,query_version) == False):
            # If GMS version has changed, get new version and push to db, return 
            # new version to variable
            # Call GMS pannel version
            return self.get_single_detailed_pannel_id(query_id,gms_pannel_version)
        else:
            return raw_data






if (__name__ == "__main__"):

    api = api_obj("arg")


    result = api.get_single_detailed_pannel(pannel_id=3,version=4.0)
    result2 = api.get_gms_pannel(3)

    print(result,"\n\n")
    print(result2)




