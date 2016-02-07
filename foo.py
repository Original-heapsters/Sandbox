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

#weight = {}
#for tag in tags:
#    if weight[tag]
#        weight[tag]

with open('tags.txt', 'w') as txt:
    for tag in tags:
        txt.write(tag + "\n")