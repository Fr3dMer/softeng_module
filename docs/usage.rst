Usage
=====
rtdtytuh hgtfytu

Installation
----------------

Install via conda::

   # Clone PanelAppDB from Github repository
   git clone https://github.com/Fr3dMer/softeng_module.git
   # Create conda environment
   conda env create -n PanelAppDB --file environment.yml
   # Activate conda environment
   conda activate PanelAppDB
   # Create directory for database
   mkdir db


Install via pip::

   # Clone PanelAppDB from Github repository
   git clone https://github.com/Fr3dMer/softeng_module.git
   # Install requirements
   # Recommend creating venv or conda environment and activating it before carrying out this step
   pip install -r docs/requirements.txt
   # Create directory for database
   mkdir db

Retreiving Pannel info
----------------

To retrieve a the gene regions covered by a pannel,
you can use the ``pannelapp.?????()`` function:

.. autofunction:: pannelapp.?????



For example:

>>> import PannelAppDB
>>> PannelAppDB.??????()
['CFTR']