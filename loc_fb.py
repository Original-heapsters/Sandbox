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
        loc_ids = self.extract_locName(json_dump)

    def extract_locName(self, json_obj):
        name = list()
        count = 0
        for line in json_obj.splitlines():
            if "name" in line:
             count += 1
             colon_index = line.find(":")
             extracted_locName = line[colon_index+2:].replace("\"","")
             name.append(extracted_locName)
        return name

    def write_location_file(self,filename):
        with open(filename,'wb') as fout:
            for name in self.names:
                fout.write(name+"\r\n")	

if __name__ == "__main__":
    fb_obj = loc_fab(token="CAACEdEose0cBAAtGRDVs7rrm8plggUrzyoQYHOmX5ZBnn5npT2yhqY4mpalZAdt8HHZCFLcGklsOZBstyQO1yeS14V8T9ZCXhLzZAtDfxLG4BDhiHiTUPowpUDZBmABOOao1piy7736jQ868ok7dDjX3LaIiLl7f181vlqseHZB8ZB0tMCoJJ2w6yG0ZCZA19nSCU2ZBEtXbsyj0IqCDZAe4ZAlm3S",user_id="758447787538137")
    
    fb_obj.init_fb()

    fb_obj.get_location_paths()
    
    fb_obj.write_location_file("location.txt")

        