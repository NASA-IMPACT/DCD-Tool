
'''
This script is to be used to identify which datasets are either 
broken and / or dropped from the Climate Data Initiative (CDI) on data.gov/climate.
Using the master list json of CDI datasets on github 
(https://raw.githubusercontent.com/fkcook/cdi_master/master/cdi_master.json), we can
ping the URLs to check their status. Broken datasets will result in a 403/404 error.
From there, we parse the working URLs for "climate5434", the tag used to identify if they are 
still in the climate theme. If not, we add those URLs along with the broken ones to the
output csv, along with their respective title, name, and cdi subthemes (Arctic, Human Health, etc)
This csv can be sent to data.gov POC to request to update the links and retag the datasets that belong 
on data.gov/climate. Manual identification can be used to identify datasets that should be removed, 
such as V2 when a V3 exists now of that dataset.
- Kane Cook 2019 (fkcook12@gmail.com)
'''
# Import packages necessary for running code
import requests
import json
import urllib
import csv

# Retrieve "CDI Master List" from GitHub
github_json = urllib.request.urlopen("https://raw.githubusercontent.com/fkcook/cdi_master/master/cdi_master.json")

# Format json contents
first_api_opener = json.load(github_json)

# Initialize headers for the CSV output
fields = ['API URL', 'Title', 'Name', 'Catalog URL', 'CDI Theme']

# Initialize containers
broken_urls = []
working_urls = []
dropped_from_cdi = []
values_container = []
api_url_list = []

# Creating CSV of Dropped URLs with their necessary values
print('[*] Starting Code [*]\n[*] Building CSV Sheet [*]')
with open('CDI_Errors.csv', 'w', newline='') as outfile:
    csvwriter = csv.DictWriter(outfile, fieldnames = fields)
    csvwriter.writeheader()
    # Loops through the GitHub raw json file looking for API URLs
    for first_json in first_api_opener:
        api_url_list.append(first_json)
        if first_json['api_url']:
           first_api = first_json['api_url']
           # If the API URL isn't healthy, it's reported
           if requests.get(first_api).status_code != 200:
              print('Found a broken link...')
              broken_urls.append(first_api)
              csvwriter.writerow({'API URL': ('BROKEN: ' + first_api), 'Title': first_json['title'], 'Name': first_json['name'], 'Catalog URL': first_json['catalog_url'], 'CDI Theme': first_json['cdi_themes']})
           else:
              # If the API URL in the raw GitHub json is healthy,
              # the code continues looking for the *next* api url
              working_urls.append(first_api)
              second_api_opener = urllib.request.urlopen(first_api)
              second_api = json.load(second_api_opener)
              if second_api['result']['groups']:
                  # Within the json, the information we need is contained in a
                  # next dictionary/loop format called "Groups"
                  groups_list = second_api['result']['groups']
                  for list_entry in groups_list:
                      values_container.append(list_entry['name'])
                  # Looks within "Groups" to check for the
                  # key value, "climate5434". If no value is found,
                  # the code reports it
                  if 'climate5434' not in values_container:
                      dropped_from_cdi.append(second_api['result']['name'])
                      csvwriter.writerow({'API URL': first_api, 'Title': second_api['result']['title'], 'Name': second_api['result']['name'], 'Catalog URL': first_json['catalog_url'], 'CDI Theme': first_json['cdi_themes']})
                      del values_container[:]
                  else:
                      del values_container[:]
              else:
                  # If "Groups" isn't found within the json, it is reported
                  dropped_from_cdi.append(second_api['result']['name'])
                  csvwriter.writerow({'API URL': first_api, 'Title': second_api['result']['title'], 'Name': second_api['result']['name'], 'Catalog URL': first_json['catalog_url'], 'CDI Theme': first_json['cdi_themes']})
        else:
            # If there isn't an API URL, it is reported (meaning it has
            # been dropped from CDI)
            csvwriter.writerow({'API URL': ('BROKEN: ' + first_api), 'Title': first_json['title'], 'Name': first_json['name'], 'Catalog URL': first_json['catalog_url'], 'CDI Theme': first_json['cdi_themes']})

# Create text files for Broken URLs and Dropped URLs
print('\n[*] Generating text files [*]')
with open('working_urls.txt', 'w') as outfile:
    for entry in working_urls:
        outfile.write(entry + '\n')
with open('broken_urls.txt', 'w') as outfile:
    for entry in broken_urls:
        outfile.write(entry + '\n')
with open('dropped_from_cdi.txt', 'w') as outfile:
    for entry in dropped_from_cdi:
        outfile.write(entry + '\n')

print("<!> COMPLETE <!>")
print("\n == List lengths == \n")
print('Total number of APIs pinged: ', len(api_url_list))
print('Total number of working URLs: ', len(working_urls))
print('Total number of broken URLs: ', len(broken_urls))
print('Total number of dropped URLs: ', len(dropped_from_cdi))
