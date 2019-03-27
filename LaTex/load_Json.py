import json
from pprint import pprint

with open('my_json_data.json') as f:
    data = json.load(f)

pprint(data)
data = data["data"]
keys = data[0].keys()
for i in data:
    print("++++++++++++++++")
    for key in keys:
        print("---------")
        print(i[key])