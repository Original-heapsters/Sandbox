import json
import facebook
import urllib2

from pprint import pprint

class fb_music:
    def __init__(self, token= None, user_id = "me", graph = None, profile = None, names= list()):
        self.token = token
        self.user_id = user_id
        self.graph = graph
        self.profile = profile
        self.names = names

    def init_fbm(self):
        self.graph = facebook.GraphAPI(self.token)
        self.profile = self.graph.get_object(self.user_id)


    def get_FbMusic_paths(self):
        feed = urllib2.urlopen("https://graph.facebook.com/v2.4/me?fields=music%7Bname%7D&access_token="+str(self.token)).read()
        parsed = json.loads(feed)
        json_dump = json.dumps(parsed, indent=4,sort_keys=True)
        music_ids = self.extract_MusicName(json_dump)

    def extract_MusicName(self, json_obj):
        name = list()
        count = 0
        for line in json_obj.splitlines():
            if "name" in line and "http" not in line:
                print("found name"+line)
                count += 1
                colon_index = line.find(":")
                extract_MusicName = line[colon_index+2:].replace("\"","")
                self.names.append(extract_MusicName)
        return name

    def write_MusicName_file(self,filename):
        with open(filename,'wb') as fout:
            for name in self.names:
                fout.write(name+"\r\n") 

if __name__ == "__main__":
    fb_obj = fb_music(token="CAACEdEose0cBAEyffWUAaTCoe5TZCNK4TI3WlMaxJx4OaIpLf47JvtBhbXlCQBUik1xnTwuS6Ny7aIJaFhZCL3TKZBTrgeDDjKmZBNEE5X0avxEMPEYrvWWGiPL4huGxoZCgAIFM5xlu8McWDikfHVZBE88RsshvZBaz0Dq90e1DLbwWiLCHsC6gJSJyRJevVuIECwCWvZBSqDMfCVv6f4I9",user_id="758447787538137")
    
    fb_obj.init_fbm()

    fb_obj.get_FbMusic_paths()
    
    fb_obj.write_MusicName_file("FB_MusicName.txt")

        