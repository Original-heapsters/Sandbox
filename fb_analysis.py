import facebook
import urllib2
import json
import string
import requests
from pprint import pprint
from nltk.corpus import stopwords

class fb_analysis:
    def __init__(self, app_id=None, app_secret=None, long_token=None, access_token=None, user_id="me", graph=None, profile=None, urls=list(), messages=list(), filename=None, names=list(),timeout=5000, proxies = None):
        self.app_id = app_id
        self.app_secret = app_secret
        self.long_token=long_token
        self.access_token = access_token
        self.user_id = user_id
        self.graph =graph
        self.profile = profile
        self.urls=urls
        self.messages=messages
        self.filename=filename
        self.names=names
        self.timeout = timeout
        self.proxies = proxies
    
    def init_fb(self):
        self.graph = facebook.GraphAPI(self.access_token)
        self.profile = self.graph.get_object(self.user_id)
                
    # Get the long urls of recent fb pictures
    def get_image_paths(self):
        feed = urllib2.urlopen("https://graph.facebook.com/v2.5/me/photos?fields=id&access_token="+str(self.access_token)).read()
        parsed = json.loads(feed)
        json_dump = json.dumps(parsed, indent=4,sort_keys=True)
        photo_ids = self.extract_ids(json_dump)
        url_list = list()
		
        # For each photo id, need to get source
        for id in photo_ids:
            url = urllib2.urlopen("https://graph.facebook.com/v2.5/"+str(id)+"?fields=images&access_token="+str(self.access_token)).read()
            parsed_url = json.loads(url)
            json_dump_url = json.dumps(parsed_url, indent=4,sort_keys=True)
            #self.extract_url(json_dump_url)
			url_list.append(extract_url(json_dump_url))
		return url_list
        
    # Get the words from recenet posts to be put into a frequency map later
    def get_message_contents(self):
        words = list()
		feed = urllib2.urlopen("https://graph.facebook.com/v2.5/me/posts?access_token="+str(self.access_token)).read()
        parsed = json.loads(feed)
        json_dump = json.dumps(parsed, indent=4,sort_keys=True)
        self.extract_messages(json_dump)
		temp = list()
		words = list()
        s=set(stopwords.words('english'))
        for line in json_dump.splitlines():
            if "message" in line:
                colon_index = line.find(":")
                extracted_msg = line[colon_index+2:].replace("\"","")
                temp.append(extracted_msg.lower().translate(None, string.punctuation))
        
        # Fileter out the stop words
        for msg in temp:
            filtered = filter(lambda w: not w in s,msg.split())
            #self.messages.append(filtered)
			words.append(filtered)
		return words
                
    # Get the users most recent location
    def get_location_paths(self):
        locations = list()
		feed = urllib2.urlopen("https://graph.facebook.com/v2.4/me?fields=location&access_token="+str(self.access_token)).read()
        parsed = json.loads(feed)
        json_dump = json.dumps(parsed, indent=4,sort_keys=True)
        #self.extract_locName(json_dump)
		for line in json_dump.splitlines():
            if "name" in line:
             colon_index = line.find(":")
             extracted_locName = line[colon_index+2:].replace("\"","")
             #self.names.append(extracted_locName)
			 locations.append(extract_locName)
		return locations
    
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
        urls = list()
        in_id = True
        biggest = True
        
        for line in json_obj.splitlines():
            #print line + str(in_id)
            if "\"id\"" in line:
                in_id = True
                
            if "source" in line and in_id:
                colon_index = line.find(":")
                extracted_url = line[colon_index+2:].replace("\"","")
                #self.urls.append(extracted_url.replace(",",""))     
				urls.append(extracted_url.replace(",",""))     
                in_id = False
		return urls
                
    # # Extract the message contents from recent posts
    # # Also remove "stop" words as defined by nltk
    # def extract_messages(self,json_obj):
        # temp = list()
		# words = list()
        # s=set(stopwords.words('english'))
        # for line in json_obj.splitlines():
            # if "message" in line:
                # colon_index = line.find(":")
                # extracted_msg = line[colon_index+2:].replace("\"","")
                # temp.append(extracted_msg.lower().translate(None, string.punctuation))
        
        # # Fileter out the stop words
        # for msg in temp:
            # filtered = filter(lambda w: not w in s,msg.split())
            # #self.messages.append(filtered)
			# words.append(filtered)
		# return words

    # # Extract the users location from the JSON result
    # def extract_locName(self, json_obj):
        # name = list()
        # for line in json_obj.splitlines():
            # if "name" in line:
             # colon_index = line.find(":")
             # extracted_locName = line[colon_index+2:].replace("\"","")
             # self.names.append(extracted_locName)
	
    # Write the results of the image urls to a file
	################UNUSED
    def write_url_file(self,filename):
        with open(filename,'wb') as fout:
            for url in self.urls:
                fout.write(url.strip()+"\r\n")
                
    # Write the results of the messages to a file
	################UNUSED
    def write_message_file(self,filename):
            with open(filename,'wb') as fout:
                for flt_words in self.messages:
                    for word in flt_words:
                        fout.write(word+"\r\n")   
                        
    # Write the users most recent location to a file
	################UNUSED
    def write_location_file(self,filename):
        with open(filename,'wb') as fout:
            for name in self.names:
                fout.write(name+"\r\n")	
   
if __name__ == "__main__":   
#app_secret='a57e46dd1a8e50677a036d0fc77e549b'
    fb_obj = fb_analysis(app_id='100000101657890',app_secret=None, user_id="100000101657890")
    fb_obj.access_token = 'CAACEdEose0cBADIRTzuZA4AGigQ4vmzkwQiNfaMgkQeut9Dspcl5YA2INfd8pLasPvhGALouzpmxjkGTQ1kqYvFVql9pMxfyiTgLCsKFCeKvCnWtuYF88nEOwvtvDt332amq9FmA6zMVuhuBbmsrzFZBzlz1nt6PTFNpY9WpxeBKKCzOuYngkXzsxgTRkRISG7ZAYWimTFaC6kfVNUD'
    fb_obj.init_fb()
    
    fb_obj.get_image_paths()
    fb_obj.get_message_contents()
    fb_obj.get_location_paths()
    
    fb_obj.write_message_file("Words.txt")
    fb_obj.write_url_file("Urls.txt")
    fb_obj.write_location_file("Location.txt")
