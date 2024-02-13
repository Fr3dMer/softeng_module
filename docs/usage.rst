Usage
=====
rtdtytuh hgtfytu

Installation
----------------
PanelAppDB can be installed using either conda or pip.
Please see below for step by step installation instructions.

**Install via conda**::

   # Clone PanelAppDB from Github repository
   git clone https://github.com/Fr3dMer/softeng_module.git
   # Create conda environment
   conda env create -n PanelAppDB --file environment.yml
   # Activate conda environment
   conda activate PanelAppDB



**Install via pip**::

   # Clone PanelAppDB from Github repository
   git clone https://github.com/Fr3dMer/softeng_module.git
   # Install requirements
   # Recommend creating venv or conda environment and activating it before carrying out this step
   pip install -r docs/requirements.txt


Retreiving Pannel Information
------------------------------
Once the tool is successfully installed, it can be used to retrieve panel information.

**Search by r-code**::

   # To search by r-code, use the -r or --rcode flag
   python PanelAppDB.py -r R45

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
   python PanelAppDB.py -p 512

This will return the same output as search by R code as outlined above.


Generate BED Files
-------------------------
PanelAppDB can be used to generate BED files for queried panels and save them locally.

**Generate GRCh37 BED Files**::

   # To generate a BED file with GRCh37 location
   


Inserting New Patient Data 
-------------------------------------------
To insert new patient information into the database, specify the patient ID number, sample ID number, R code of the panel applied and the database location.

-r or --rcode specified the panel applied to the patient testing
-pid or --patientID specifies the patient ID to insert
-sid or --sampleID specifies the sample ID to insert
-f or --fdb specifies the local database location to insert data into


**Insert Patient Data**::

   # To insert patient data use the flags listed above
   python PanelAppDB.py -r R46 -pid 133 -sid 433 -f 'db/'


Search for Patient Data
-------------------------
Patient data can be searched by patient ID number.

**Search by Patient ID**::

   # To search for patient records, use -g or --get_patient_data flags to specify the patient ID
   python PanelAppDB.py -g 124 -f 'db/'


