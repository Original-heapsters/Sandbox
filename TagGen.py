import os
import json
import sys
import fb_analysis

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
    
    fb_obj = fb_analysis(app_id='100000101657890',app_secret=None, user_id="100000101657890")
    fb_obj.access_token = 'CAACEdEose0cBAGwZBqL0gBFqVsX4ZC8rnZA5tjAZARJ70IljId0DD1Wc3ZA9WV6gU6gEghIjEiZBeJtYpdCkBLJTkQH542UkUxGiHiyjkzcnjcT28khX9r9Yc18Xp6kMEknpRV54ypNVcuTqn5SAVRA8r8kTloCff7ezFtfprDyWZCck8PgYrFORhvoL5fEzXTAc3E5KcuTM1ejjNxfQ6jZC'
    fb_obj.init_fb()
    
    fb_obj.get_image_paths()
    fb_obj.get_message_contents()
    fb_obj.get_location_paths()
    
    fb_obj.write_message_file("Words.txt")
    fb_obj.write_url_file("Urls.txt")
    fb_obj.write_location_file("Location.txt")

    txtfile = sys.argv
    tags = []
    weight = dict();
    with open(txtfile[1], 'r') as link:
        for x in link:
            main(x, tags)

    add_tags(weight, tags)

    tags = []
    with open('Words.txt', 'r') as txt:
        for x in txt:
            tags.append(x.strip())
    add_tags(weight,tags)
    
    location = []
    with open('Location.txt', 'r') as txt:
        for x in txt:
            location.append(x.strip().split(",")[0])

    with open('weightedTag.txt', 'w') as f:
        for w in sorted(weight, key = weight.get, reverse = True):
           f.write(w + "\n")

    with open('weightedTag.txt', 'r') as f:
        with open('keywords.txt', 'w') as w:
            count = 0
            max_count = 11
            min_count = 4
            for line in f:
                if count in range(min_count, max_count):
                    w.write(location[0] + "," + line)
                count += 1
            