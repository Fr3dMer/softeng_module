"""****************************************************************************
File          : PannelAppDB.py
About         : Hold main logical flow for app 
Author        : Freddie Mercer
****************************************************************************"""

import src.api as api_module





def main():

    # CLI 

    # Instantiate api obj

    api = api_module.api_obj("args")
   
    # Check internet connection 
    if(api.check_internet()):
        internet = True
    else:
        internet = False

    # Needs call pannel from db, returning version 

    # Make a call to API and get GMS version 
    gms_pannel = api.get_gms_pannel(3)

    # Compare versions

    # If GMS version has changed, get new version and push to db, return new version to variable

    # If not changed, return version in db to variable 

    # Taken in by parser


    pass






if (__name__ == "__main__"):

   main()





