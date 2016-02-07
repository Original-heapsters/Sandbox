import json
import facebook
import urllib2

from pprint import pprint

class loc_fab:
    def __init__(self, token= None, user_id = "me", graph = None, profile = None, names= list()):
        self.token = token
        self.user_id = user_id
        self.graph = graph
        self.profile = profile
        self.names = names

    def init_fb(self):
        self.graph = facebook.GraphAPI(self.token)
        self.profile = self.graph.get_object(self.user_id)


    def get_location_paths(self):
        feed = urllib2.urlopen("https://graph.facebook.com/v2.4/me?fields=location&access_token="+str(self.token)).read()
        parsed = json.loads(feed)
        json_dump = json.dumps(parsed, indent=4,sort_keys=True)
        self.extract_locName(json_dump)

    def extract_locName(self, json_obj):
        name = list()
        for line in json_obj.splitlines():
            if "name" in line:
             colon_index = line.find(":")
             extracted_locName = line[colon_index+2:].replace("\"","")
             self.names.append(extracted_locName)

    def write_location_file(self,filename):
        with open(filename,'wb') as fout:
            for name in self.names:
                fout.write(name+"\r\n")	

if __name__ == "__main__":
    fb_obj = loc_fab(token="CAACEdEose0cBAHv0pn3hY63Y5GznI8c109PL6zVVCu8TOV9qirQO2QtYSXnxoBZBZAGsJVBi0k1ISqaK2t73ZAcCTkX5ZBT6SVlZCJcsMDFlOKzZCm9iji7BT8KWVfwy2J2hKqrZAP1oUAAZBNINYv7gFZAZCff5HlbwXj6Sr0OZA57xU3IYmEZBlSQbVd0QZA7EeeHLZAo1ja1OYq40KNXAGkSRdc",user_id="758447787538137")
    
    fb_obj.init_fb()

    fb_obj.get_location_paths()
    
    fb_obj.write_location_file("location.txt")

        