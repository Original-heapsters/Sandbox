import os
import json
import sys
from pprint import pprint
from pyshorteners import Shortener

def main(argv):
    print "Inside check"
    if len(argv) > 1:
        url = argv
        if len(argv) > 20:
            shortener = Shortener('TinyurlShortener')
            print url
            url = shortener.short(url.strip())
            
    else:
        print("ERROR")
        url = "http://www.clarifai.com/img/metro-north.jpg"

    command = 'curl -H "Authorization: Bearer b3A9PCVEzVkAijC1CC0qEUPNKcS9GE" --data-urlencode "url='
    command = command + url + '" https://api.clarifai.com/v1/tag/'
    command = command + " | python -mjson.tool > test.json"
    print "Trying " + command
    os.system(command)

    with open('test.json') as test:
        data = json.load(test)

    pprint(data['results'][0]['result']['tag']['classes']) 

if __name__ == '__main__':
    txtfile = sys.argv
    print "Inside checks main"
    with open(txtfile[1], 'r') as link:
        for x in link:
            main(x)