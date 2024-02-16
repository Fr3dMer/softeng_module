Usage
=====
PanelAppDB can be run in the conda environent created in the steps above, or in a Docker container.

Running script localy using conda environment
----------------------------------------------
To run in the conda enviroment, ensure the environment is activated and submit your desired query using the corresponding arguments (discussed below). eg::

   conda activate PanelAppDB
   python panel_app_db.py <PARAMS HERE>
   # Example:
   python panel_app_db.py -r R45

Building and running script inside container
---------------------------------------------
To run in a container, build the container in docker then run it with docker run. eg: ::

   sudo docker build --rm -t "panel_app_db" .
   sudo docker run --rm panel_app_db <PARAMS HERE>
   # example:
   sudo docker run --rm panel_app_db -r R45 

Retreiving Pannel Information
------------------------------
Once the tool is successfully installed, it can be used to retrieve panel information.

**Search by r-code**::

   # To search by r-code, use the -r or --rcode flag
   python panel_app_db.py -r R45

This will return the panel id, Version, disease code and a table of gene regions covered by the panel.::

   Panel id :           3
   Version :            4.0
   Disease:             R45
   Last updated:        2023-03-22
   |    | HGNC Symbol   | HGNC ID    | GRch38 location       |
   |---:|:--------------|:-----------|:----------------------|
   |  0 | BMP4          | HGNC:1071  | 14:53949736-53958761  |
   |  1 | COL11A1       | HGNC:2186  | 1:102876467-103108496 |
   |  2 | COL11A2       | HGNC:2187  | 6:33162681-33192499   |
   |  3 | COL2A1        | HGNC:2200  | 12:47972965-48004486  |
   |  4 | COL9A1        | HGNC:2217  | 6:70215061-70303083   |
   |  5 | COL9A2        | HGNC:2218  | 1:40300487-40317816   |
   |  6 | COL9A3        | HGNC:2219  | 20:62816244-62841159  |
   |  7 | GZF1          | HGNC:15808 | 20:23362182-23373063  |
   |  8 | VCAN          | HGNC:2464  | 5:83471465-83582303   |
   |  9 | LOXL3         | HGNC:13869 | 2:74532414-74555690   |
   | 10 | LRP2          | HGNC:6694  | 2:169127109-169362685 |

**Search by PanelApp ID**::

   #To search by the PanelApp ID number, use -p or --panel_id flags
   python panel_app_db.py -p 512

This will return the same output as search by R code as outlined above.


Generate BED Files
-------------------------
PanelAppDB can be used to generate BED files for queried panels and save them locally.


**Generate GRCh37 BED Files**::

   # Use -b37 or --bed37 to specify the path and desired BED filename
   python panel_app_db.py -r R45 -b37 'db/R45_v1.bed'

This example will generate a bed file using GRCh37 loci for the current R45 panel and save it locally with a path of db/R45_v1.bed.

**Generate GRCh38 BED Files**::

   # Use -b38 or --bed38 to specify the path and desired BED filename
   python panel_app_db.py -r R45 -b38 'db/R45_v1.bed'


This example will generate a bed file using GRCh38 loci for the current R45 panel and save it locally with a path of db/R45_v1.bed.
   


Inserting New Patient Data 
-------------------------------------------
To insert new patient information into the database, specify the patient ID number, sample ID number, R code of the panel applied and the database location.

-r or --rcode specified the panel applied to the patient testing
-pid or --patientID specifies the patient ID to insert
-sid or --sampleID specifies the sample ID to insert
-f or --fdb specifies the local database location to insert data into


**Insert Patient Data**::

   # To insert patient data use the flags listed above
   python panel_app_db.py -r R46 -pid 133 -sid 433 -f 'db/'


Search for Patient Data
-------------------------
Patient data can be searched by patient ID number.


**Search by Patient ID**::

   # To search for patient records, use -g or --get_patient_data flags to specify the patient ID
   python panel_app_db.py -g 124 -f 'db/'



Run in Debug mode 
------------------
The module can be run in debug mode by using the -d or --debug_mode flags

**Debug Mode**::

   # To search for a panel in debug mode use the -d flag
   python panel_app_db.py -r R46 -d