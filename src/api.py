"""****************************************************************************
File          : api.py
About         : Object for interacting with pannelapp api 
Author        : Freddie Mercer
Date modified : 2023-12-08
****************************************************************************"""

import requests


class api_obj():

    def __init__(self, logger):
        self.log = logger

    def get_gms_pannel(self, panel_id):
        """Fetches the signed-off panel from the Genomics England 
        PanelApp API.

        Parameters:
        panel_id (int): The ID of the panel to fetch. T

        Returns:
        dict: The response from the API, parsed as a JSON dictionary.
              This will contain the data for the requested panel.

        Raises:
        ValueError: If the provided panel_id does not meet the required
                    format.

        Note:
        Before making the API request, this function validates the 
        format of the panel_id using the value_checker method.
        It then constructs the URL for the API request and logs a 
        debug message. Finally, it makes the GET request to the API and
        returns the response.
        """
        
        # Check correct format 
        self.value_checker(panel_id=panel_id)
        # Construct url
        url = ('https://panelapp.genomicsengland.co.uk/api/'
               'v1/panels/signedoff/') + str(panel_id)
        self.log.logger.debug("API request for latest GMS panel")
        # Call api and return results 
        return requests.get(url).json()

    def get_single_detailed_pannel_id(self,panel_id, version=None):
        """Fetches detailed information about a specific panel 
        from the Genomics England PanelApp API.

        Parameters:
        pannel_id (int): The ID of the panel to fetch.
        version (float, optional): The version of the panel to fetch. 
                                    If not provided, the function will 
                                    fetch the latest version.

        Returns:
        dict: The response from the API, parsed as a JSON dictionary. 
              This will contain the detailed data for the 
              requested panel.

        Raises:
        ValueError: If the provided pannel_id or version does 
                    not meet the required format.

        Note:
        If no version is provided, the function constructs 
        the URL for the API request without specifying a 
        version, and makes a GET request to the API.
        If a version is provided, the function validates the 
        format of the version and pannel_id using the value_checker 
        method, constructs the URL for the API request with the specified 
        version, and makes a GET request to the API.
        """
        
        if(version == None):
            url = ("https://panelapp.genomicsengland.co.uk/api"
                   "/v1/panels/") + str(panel_id) 
            self.log.logger.debug("API request for latest panel")
            return requests.get(url).json()

        self.value_checker(version = version, panel_id = panel_id)
        url = ("https://panelapp.genomicsengland.co.uk/"
               "api/v1/panels/") + str(panel_id) + "/"       
        payload = {'version':version} 
        self.log.logger.debug("API request for panel")
        return requests.get(url,params = payload).json()

    def get_single_detailed_pannel_rcode(self, rcode, version=None):
        """Fetches detailed information about a specific panel from 
        the Genomics England PanelApp API using the panel's rcode.

        Parameters:
        rcode (str): The rcode of the panel to fetch.
        version (float, optional): The version of the panel 
                                   to fetch. If not provided, 
                                   the function will fetch the 
                                   latest version.

        Returns:
        dict: The response from the API, parsed as a JSON dictionary. 
              This will contain the detailed data for the requested 
              panel.

        Raises:
        ValueError: If the provided rcode or version does not 
                    meet the required format.

        Note:
        The function validates the format of the rcode and version 
        using the value_checker method, constructs the URL for the API 
        request with the specified rcode, and makes a GET request to the 
        API.
        """
        
        self.value_checker(version = version, rcode = rcode)

        url = ("https://panelapp.genomicsengland.co.uk/api"
               "/v1/panels/") + str(rcode) 
        self.log.logger.debug("API request for panel")
        return requests.get(url).json()


    def value_checker(self, panel_id=None, version=None, rcode=None):
        """Validates the types of the provided panel_id, version, 
        and rcode values.

        Parameters:
        panel_id (int, optional): The ID of the panel.
        version (float or str, optional): The version of the panel. 
        rcode (str, optional): The rcode of the panel.

        Raises:
        ValueError: If the provided panel_id, version, or rcode does 
                    not meet the required format.

        Note:
        This function is used to ensure that the values passed to 
        other functions are in the correct format.
        It checks the type of each parameter and raises a ValueError 
        if a parameter is not of the expected type.
    """

        if not(version == None 
               or type(version) == float 
               or type(version) == str):
            error_str = ("Internal error: incorrect value type for version "
                        "used for api cal, please use a string or float")
            self.log.logger.error(error_str)
            raise ValueError
      
        if not(panel_id == None 
               or type(panel_id) == int):
            error_str = ("Internal error: incorrect value type for "
                         "panel id used for api call, please use a int")
            self.log.logger.error(error_str)
            raise ValueError
        
        if not(rcode == None 
               or type(rcode) == str):
            error_str = ("Internal error: incorrect value type for "
                         "rcode used for api call, please provide a str")
            self.log.logger.error(error_str)
            raise ValueError
    
    def version_check(self, query_version, true_version):
        """Compares two version numbers to determine 
        if they are equal.

        Parameters:
        query_version (float): The version number to 
                                compare against the true version.
        true_version (float): The true version number.

        Returns:
        bool: True if the query_version is equal to the true_version, 
              False otherwise.

        Raises:
        SyntaxError: If either of the provided version numbers is 
                     not a float.

        Note:
        This function first checks if both version numbers 
        are floats. If not, it raises a SyntaxError.
        It then compares the two version numbers and returns 
        True if they are equal and False otherwise.
        """

        if not (type(query_version) == float and type(true_version) == float):
            error_str = ("Verions are not floats, cannot compare versions")
            self.log.logger.error(error_str)
            raise SyntaxError

        if(query_version == true_version):                        
            return True

        elif(query_version != true_version):
            return False

    def check_internet(self,url='http://google.com'):
        """Checks the internet connection by attempting to access 
        a specified URL.

        Parameters:
        url (str, optional): The URL to attempt to access. 
                            Defaults to 'http://google.com'.

        Returns:
        bool: True if the URL could be accessed within the 
              timeout period, False otherwise.

        Note:
        This function attempts to send a GET request to the specified 
        URL with a timeout of 5 seconds.
        If the request is successful, the function returns True, 
        indicating that there is an active internet connection.
        If the request fails (for example, due to a timeout or 
        network error), the function catches the exception and 
        returns False, indicating that there may not be an active
          internet connection.
        """
        
        try:
            response = requests.get(url, timeout = 5)
        except:
            return False
        else:
            return True
    
    def get_gms_versions(self, raw_data, parser):
        """Extracts the version from the raw data, fetches 
        the most recent GMS panel from the API, and compares the 
        versions.

        Parameters:
        raw_data (dict): The raw data containing the panel information.
        parser (obj): An object with methods to extract the version and 
                      panel ID from the raw data.

        Returns:
        dict: If the GMS panel version matches the query version, 
              the original raw data is returned.
              If the GMS panel version does not match the query 
              version, the updated panel data is returned.

        Raises:
        ValueError: If the extracted version or panel ID 
                    is not in the correct format.

        Note:
        This function first extracts the version and panel 
        ID from the raw data using the provided parser object.
        It then fetches the most recent GMS panel from the API 
        using the extracted panel ID.
        The function compares the fetched GMS panel version with the 
        extracted query version.
        If the versions do not match, the function fetches the updated 
        panel data and returns it.
        If the versions match, the function returns the original
        raw data.
        """

        # Make a call to API and get GMS version
        query_version = float(parser.extract_version(raw_data))
        query_id = int(parser.extract_panel_id(raw_data))
        gms_panel = self.get_gms_pannel(query_id)
        gms_pannel_version = float(gms_panel.get("version",None))

        # Compare versions
        if(self.version_check(gms_pannel_version,query_version) == False):
            # If GMS version has changed, get new 
            # version and push to db, return 
            # new version to variable
            # Call GMS pannel version
            return self.get_single_detailed_pannel_id(query_id, 
                                                      gms_pannel_version)
        else:
            return raw_data
