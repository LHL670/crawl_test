import json
 
# Opening JSON file
f = open('service-account.json',)
 
# returns JSON object as
# a dictionary
data = json.load(f)
 
# Iterating through the json
# list
for i in data['type']:
    print(i)
 
# Closing file
f.close()