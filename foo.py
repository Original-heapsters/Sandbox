import os
import json
import sys
from pprint import pprint
from pyshorteners import Shortener

os.system("python check.py test_url.txt > tag.txt")

tags = []
with open('tag.txt', 'r') as txt:
    for x in txt:
        tags.append(x.split("'")[1])

with open('tags.txt', 'w') as txt:
    for tag in tags:
        txt.write(tag + "\n")