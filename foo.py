import os
import json
import sys
from pprint import pprint
from pyshorteners import Shortener

txt = sys.argv[1]

command = "python check.py " + txt + " > tag.txt"
os.system( command )

tags = []
with open('tag.txt', 'r') as txt:
    for x in txt:
        tags.append(x.split("'")[1])

weight = dict()
for tag in tags:
    if weight.get(tag, "empty") == ("empty"):
        weight[tag] = 1
    else:
        weight[tag] += 1
    
for w in sorted(weight, key = weight.get, reverse = True):
    print(w, weight[w])

with open('tags.txt', 'w') as txt:
    for w in sorted(weight, key = weight.get, reverse = True):
        txt.write(str(w) + " " + str(weight[w]) + "\n")
    # for tag in tags:
    #     txt.write(tag + "\n")