Usage
=====
rtdtytuh hgtfytu

Installation
----------------

Install via conda::

   # Clone PanelAppDB from Github repository
   git clone https://github.com/Fr3dMer/softeng_module.git
   conda env create -n PanelAppDB --file environment.yml
   conda activate PanelAppDB
   mkdir db


Install via pip::

   git clone https://github.com/Fr3dMer/softeng_module.git
   # Recommend creating venv or conda environment and activating it before carrying out this step
   pip install -r docs/requirements.txt
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