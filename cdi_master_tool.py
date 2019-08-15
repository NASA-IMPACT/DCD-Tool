
'''
We want to take CDI API URLS from json master list and parse them.
Then, we search for the tag in the list that uses "climate5434", with 2 possible
output values. The first is TRUE, meaning climate5434 is present, therefore
tagged in data.gov/climate appropriately. The second is FALSE, which means
climate5434 is not present and needs to be retagged. There will be some URL's
are broken or have a value of NONE, so first we must subtract those values
from the whole list and only run valid URLs. You can create a list of broken
ones to perform QA on and add the correct ones back into the master list,
effectively adding them back into valid API URLs.
- Kane Cook 2019
'''
# Import packages necessary for running code
import requests
import json
import urllib
import csv

# Retrieve "CDI Master List" from GitHub
github_json = urllib.request.urlopen("https://raw.githubusercontent.com/fkcook/cdi_master/master/cdi_master.json")

# Format json contents
json_reader = json.load(github_json)

# Format CSV output
fields = [['API URL', 'Title', 'Name', 'Catalog URL', 'CDI Theme']]

# Initialize containers
broken_urls = []
working_urls = []
dropped_from_cdi = []
values_container = []
api_url_list = []

# Loop through and remove links and "None" values
print('[*] Starting Code [*]')
for first_json in json_reader:
    api_url_list.append(first_json)
    if first_json['api_url']:
       first_api = first_json['api_url']
       if requests.get(first_api).status_code != 200:
          print('Found a broken link...')
          broken_urls.append(first_api)
       else:
          working_urls.append(first_api)
          second_api_opener = urllib.request.urlopen(first_api)
          second_api = json.load(second_api_opener)
          if second_api['result']['groups']:
              groups_list = second_api['result']['groups']
              for list_entry in groups_list:
                  values_container.append(list_entry['name'])
              if 'climate5434' not in values_container:
                  dropped_from_cdi.append(second_api['result']['name'])
                  del values_container[:]
              else:
                  del values_container[:]
          else:
              dropped_from_cdi.append(second_api['result']['name'])
    else:
        broken_urls.append(first_api)

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
