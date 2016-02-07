import os
import json
import sys
from pprint import pprint
from pyshorteners import Shortener


def add_tags(dict, more_tags=list()):
    for tag in more_tags:
        if dict.get(tag, "empty") == ("empty"):
            dict[tag] = 1
        else:
            dict[tag] += 1


txt = sys.argv[1]

command = "python check.py " + txt + " > tag.txt"
os.system( command )
print "done with command"
# Tags returned from clarifai
tags = []
with open('tag.txt', 'r') as txt:
    for x in txt:
        tags.append(x.split("'")[1])


weight = dict()
add_tags(weight,tags)

tags = []
with open('Words.txt', 'r') as txt:
    for x in txt:
        tags.append(x)
add_tags(weight,tags)
tags = []
with open('Location.txt', 'r') as txt:
    for x in txt:
        tags.append(x)
add_tags(weight,tags)
#for tag in tags:
#    if weight.get(tag, "empty") == ("empty"):
#        weight[tag] = 1
#    else:
#        weight[tag] += 1
    
for w in sorted(weight, key = weight.get, reverse = True):
    print(w, weight[w])

with open('tags.txt', 'w') as txt:
    for w in sorted(weight, key = weight.get, reverse = True):
        txt.write(str(w) + " " + str(weight[w]) + "\n")
    # for tag in tags:
    #     txt.write(tag + "\n")