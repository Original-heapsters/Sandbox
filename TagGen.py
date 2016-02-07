import os
import json
import sys
from pprint import pprint
from pyshorteners import Shortener

def main(argv, list_of_tags):
    if len(argv) > 1:
        url = argv
        if len(argv) > 20:
            shortener = Shortener('TinyurlShortener')
            url = shortener.short(url.strip())
    else:
        print("ERROR")
        url = "http://www.clarifai.com/img/metro-north.jpg"

    command = 'curl -H "Authorization: Bearer b3A9PCVEzVkAijC1CC0qEUPNKcS9GE" --data-urlencode "url='
    command = command + url + '" https://api.clarifai.com/v1/tag/'
    command = command + " | python -mjson.tool > test.json"
    os.system(command)

    with open('test.json') as test:
        data = json.load(test)

    with open('tag.txt', 'w') as f:
        pprint(data['results'][0]['result']['tag']['classes'], f)

    with open('tag.txt', 'r') as f:
        for x in f:
            list_of_tags.append(x.split("'")[1]) 

    
def add_tags(dict, more_tags=list()):
    for tag in more_tags:
        if dict.get(tag, "empty") == ("empty"):
            dict[tag] = 1
        else:
            dict[tag] += 1


if __name__ == '__main__':
    txtfile = sys.argv
    tags = []
    weight = dict();
    with open(txtfile[1], 'r') as link:
        for x in link:
            main(x, tags)

    add_tags(weight, tags)

    for w in sorted(weight, key = weight.get, reverse = True):
       print(w, weight[w])

