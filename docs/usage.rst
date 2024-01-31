Usage
=====
rtdtytuh hgtfytu

Installation
----------------

To use PannelAppDB, first install it using pip:

.. code-block:: console

   (.venv) $ pip install PannelAppDB

   ## Install via conda
   ```bash
   git clone https://github.com/Fr3dMer/softeng_module.git
   conda env create -n PanelAppDB --file environment.yml
   conda activate PanelAppDB
   mkdir db
   ```

   ## Install via pip
   - This section has been added to satisfy the rebric 
   ```bash
   git clone https://github.com/Fr3dMer/softeng_module.git
   # Recommend creating venv or conda environment and activating it before carrying out this step
   pip install -r docs/requirements.txt
   mkdir db
   ```
Retreiving Pannel info
----------------

To retrieve a the gene regions covered by a pannel,
you can use the ``pannelapp.?????()`` function:

.. autofunction:: pannelapp.?????



For example:

>>> import PannelAppDB
>>> PannelAppDB.??????()
['CFTR']