# DCD-Tool

This script is to be used to identify which datasets are either 
broken and / or dropped from the Climate Data Initiative (CDI) on data.gov/climate.
Using the master list json of CDI datasets on github 
(https://github.com/NASA-IMPACT/cdi_master/blob/master/cdi_master.json), we can
ping the URLs to check their status. Broken datasets will result in a 403/404 error.
From there, we parse the working URLs for "climate5434", the tag used to identify if they are 
still in the climate theme. If not, we add those URLs along with the broken ones to the
output csv, along with their respective title, name, and cdi subthemes (Arctic, Human Health, etc)
This csv can be sent to data.gov POC to request to update the links and retag the datasets that belong 
on data.gov/climate. Manual identification can be used to identify datasets that should be removed, 
such as V2 when a V3 exists now of that dataset.

## Running the tool
1. Download the repository onto local machine.

2. Pip install required libaries:
- requests
- urllib

3. Navigate to necessary directory:
`$python cdi_master_tool.py`
