
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
raw_json = urllib.request.urlopen("https://raw.githubusercontent.com/fkcook/cdi_master/master/cdi_master.json")

# Format json contents
json_reader = json.load(raw_json)

# Format CSV output
fields = [['API URL', 'Title', 'Name', 'Catalog URL', 'CDI Theme']]

# Initialize containers
broken_urls = []
working_urls = []
dropped_urls = []
values_container = []
api_url_list = []

# Loop through and remove links and "None" values
print('[*] Starting Code [*]')
with open('CDI_CSV_Output.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(fields)
    for json_entry in json_reader:
        api_url_list.append(json_entry)
        if json_entry['api_url']:
           api_url = json_entry['api_url']
           if requests.get(api_url).status_code != 200:
              print('Found a broken link...')
              broken_urls.append(api_url)
           else:
              prepped_api = urllib.request.urlopen(api_url)
              opened_api = json.load(prepped_api)
              if opened_api['result']['groups']:
                  groups_list = opened_api['result']['groups']
                  for list_entry in groups_list:
                      values_container.append(list_entry['name'])
                  if 'climate5434' not in values_container:
                      print(opened_api['result']['name'])
                      dropped_urls.append(opened_api['result']['name'])
                      csvwriter = [[api_url, json_entry['title'], json_entry['name'], json_entry['cdi_themes']]]
                      del values_container[:]
                  else:
                      del values_container[:]
              else:
                  print(opened_api['result']['name'])
                  dropped_urls.append(opened_api['result']['name'])
        else:
            broken_urls.append(json_entry)

# Create text files for Broken URLs and Dropped URLs
print('\n[*] Generating "broken_urls.txt" and "dropped_urls.txt" [*]')
with open('broken_urls.txt', 'w') as broken_textfile:
    for entry in broken_urls:
        broken_textfile.write(entry + '\n')
with open('dropped_urls.txt', 'w') as dropped_textfile:
    for entry in dropped_urls:
        dropped_textfile.write(entry + '\n')

print("<!> COMPLETE <!>")
print("\n == List lengths == \n")
print('Total number of APIs pinged: ', len(api_url_list))
print('Total number of broken URLs: ', len(broken_urls))
print('Total number of dropped URLs: ', len(dropped_urls))
