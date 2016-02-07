import os
import json
from pprint import pprint

url = "http://www.clarifai.com/img/metro-north.jpg"
command = 'curl -H "Authorization: Bearer b3A9PCVEzVkAijC1CC0qEUPNKcS9GE" --data-urlencode "url=http://www.clarifai.com/img/metro-north.jpg"  https://api.clarifai.com/v1/tag/'
command = command + "| python -mjson.tool > test.json"
os.system(command)

with open('test.json') as test:
    data = json.load(test)

pprint(data['results'][0]['result']['tag']['classes'])