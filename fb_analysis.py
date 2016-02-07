import facebook
import urllib2
import json
from pprint import pprint

class fb_analysis:
	def __init__(self, token=None, user_id="me", graph=None, profile=None, urls=list(), messages=list(), filename=None):
		self.token = token
		self.user_id = user_id
		self.graph =graph
		self.profile = profile
		self.urls=urls
		self.messages=messages
		self.filename=filename
	
    def init_fb(self):
        self.graph = facebook.GraphAPI(self.token)
        self.profile = self.graph.get_object(self.user_id)
    
	def get_image_paths(self):
		
		feed = urllib2.urlopen("https://graph.facebook.com/v2.5/me/photos?fields=id&access_token="+str(self.token)).read()
		parsed = json.loads(feed)
		json_dump = json.dumps(parsed, indent=4,sort_keys=True)
		photo_ids = self.extract_ids(json_dump)
		
		for id in photo_ids:
			url = urllib2.urlopen("https://graph.facebook.com/v2.5/"+str(id)+"?fields=images&access_token="+str(self.token)).read()
			parsed_url = json.loads(url)
			json_dump_url = json.dumps(parsed_url, indent=4,sort_keys=True)
			self.extract_url(json_dump_url)
		
		for url in self.urls:
			print url
	
	def get_message_contents(self):
		feed = urllib2.urlopen("https://graph.facebook.com/v2.5/me/posts?access_token="+str(self.token)).read()
		parsed = json.loads(feed)
		json_dump = json.dumps(parsed, indent=4,sort_keys=True)
		self.extract_messages(json_dump)
		
		for message in self.message:
			print message
		
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
				
	def extract_messages(self,json_obj):
		messages = list()
		for line in json_obj.splitlines():
			if "message" in line:
				colon_index = line.find(":")
				extracted_msg = line[colon_index+2:].replace("\"","")
				self.messages.append(extracted_msg)		
	
	def write_url_file(self,filename):
		with open(filename,'wb') as fout:
			for url in self.urls:
				fout.write(url.strip()+"\r\n")
				
	def write_message_file(self,filename):
			with open(filename,'wb') as fout:
				for msg in self.messages:
					fout.write(msg.strip()+"\r\n")				
        
		
		
if __name__ == "__main__":
	
    fb_obj = fb_analysis(token="CAACEdEose0cBAKBftO3m9N1almhKoEx1Hw67kP4kBBrPBaZAZBM6Db4TqXZCNjuZBtyYGlfiSe9ccVjtaNZAJXFGRGcOgHhKZBOPZCDf52baoDXyje2G6UXJjHgN8ioK9FBWfTVtBuexWBkkf2uwNHpsPade3IurhL6uzBZAgqv5cbc7ZAXJOZBg7PTzlBg8v2BU0EYYiw1CFNeD3b4voreim2", user_id="100000101657890")
	
	fb_obj.init_fb()
	
	fb_obj.get_image_paths()
	fb_obj.get_message_contents()
	
	fb_obj.write_url_file("Urls.txt")