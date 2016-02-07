import facebook
import urllib2
import json
import string
from pprint import pprint
from nltk.corpus import stopwords

class fb_analysis:
    def __init__(self, token=None, user_id="me", graph=None, profile=None, urls=list(), messages=list(), filename=None, names=list()):
        self.token = token
        self.user_id = user_id
        self.graph =graph
        self.profile = profile
        self.urls=urls
        self.messages=messages
        self.filename=filename
        self.names=names
    
    def init_fb(self):
        self.graph = facebook.GraphAPI(self.token)
        self.profile = self.graph.get_object(self.user_id)
        
    # Get the long urls of recent fb pictures
    def get_image_paths(self):
        feed = urllib2.urlopen("https://graph.facebook.com/v2.5/me/photos?fields=id&access_token="+str(self.token)).read()
        parsed = json.loads(feed)
        json_dump = json.dumps(parsed, indent=4,sort_keys=True)
        photo_ids = self.extract_ids(json_dump)
        
        # For each photo id, need to get source
        for id in photo_ids:
            url = urllib2.urlopen("https://graph.facebook.com/v2.5/"+str(id)+"?fields=images&access_token="+str(self.token)).read()
            parsed_url = json.loads(url)
            json_dump_url = json.dumps(parsed_url, indent=4,sort_keys=True)
            self.extract_url(json_dump_url)
        
    # Get the words from recenet posts to be put into a frequency map later
    def get_message_contents(self):
        feed = urllib2.urlopen("https://graph.facebook.com/v2.5/me/posts?access_token="+str(self.token)).read()
        parsed = json.loads(feed)
        json_dump = json.dumps(parsed, indent=4,sort_keys=True)
        self.extract_messages(json_dump)
                
    # Get the users most recent location
    def get_location_paths(self):
        feed = urllib2.urlopen("https://graph.facebook.com/v2.4/me?fields=location&access_token="+str(self.token)).read()
        parsed = json.loads(feed)
        json_dump = json.dumps(parsed, indent=4,sort_keys=True)
        self.extract_locName(json_dump)
    
    # Extract the image ids from the psuedo JSON result
    def extract_ids(self,json_obj):
        ids = list()
        count = 0
        for line in json_obj.splitlines():
            if "id" in line and "http" not in line:
                count += 1
                colon_index = line.find(":")
                extracted_id = line[colon_index+2:].replace("\"","")
                ids.append(extracted_id)        
        return ids
        
    # Extract the image url from the JSON result
    def extract_url(self,json_obj):
        url = list()
        in_id = True
        biggest = True
        
        for line in json_obj.splitlines():
            #print line + str(in_id)
            if "\"id\"" in line:
                in_id = True
                
            if "source" in line and in_id:
                colon_index = line.find(":")
                extracted_url = line[colon_index+2:].replace("\"","")
                self.urls.append(extracted_url.replace(",",""))     
                in_id = False
                
    # Extract the message contents from recent posts
    # Also remove "stop" words as defined by nltk
    def extract_messages(self,json_obj):
        temp_list = list()
        s=set(stopwords.words('english'))
        for line in json_obj.splitlines():
            if "message" in line:
                colon_index = line.find(":")
                extracted_msg = line[colon_index+2:].replace("\"","")
                temp_list.append(extracted_msg.lower().translate(None, string.punctuation))#self.messages.append(extracted_msg)     
        
        # Fileter out the stop words
        for msg in temp_list:
            filtered = filter(lambda w: not w in s,msg.split())
            self.messages.append(filtered)

    # Extract the users location from the JSON result
    def extract_locName(self, json_obj):
        name = list()
        for line in json_obj.splitlines():
            if "name" in line:
             colon_index = line.find(":")
             extracted_locName = line[colon_index+2:].replace("\"","")
             self.names.append(extracted_locName)
            
    # Write the results of the image urls to a file
    def write_url_file(self,filename):
        with open(filename,'wb') as fout:
            for url in self.urls:
                fout.write(url.strip()+"\r\n")
                
    # Write the results of the messages to a file
    def write_message_file(self,filename):
            with open(filename,'wb') as fout:
                for flt_words in self.messages:
                    for word in flt_words:
                        fout.write(word+"\r\n")   
                        
    # Write the users most recent location to a file
    def write_location_file(self,filename):
        with open(filename,'wb') as fout:
            for name in self.names:
                fout.write(name+"\r\n")	                        
        
if __name__ == "__main__":   
    fb_obj = fb_analysis(token="CAACEdEose0cBAHv0pn3hY63Y5GznI8c109PL6zVVCu8TOV9qirQO2QtYSXnxoBZBZAGsJVBi0k1ISqaK2t73ZAcCTkX5ZBT6SVlZCJcsMDFlOKzZCm9iji7BT8KWVfwy2J2hKqrZAP1oUAAZBNINYv7gFZAZCff5HlbwXj6Sr0OZA57xU3IYmEZBlSQbVd0QZA7EeeHLZAo1ja1OYq40KNXAGkSRdc", user_id="100000101657890")
    fb_obj.init_fb()
    
    fb_obj.get_image_paths()
    fb_obj.get_message_contents()
    fb_obj.get_location_paths()
    
    fb_obj.write_message_file("Words.txt")
    fb_obj.write_url_file("Urls.txt")
    fb_obj.write_location_file("Location.txt")
