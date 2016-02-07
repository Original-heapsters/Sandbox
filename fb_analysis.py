import facebook
import json

class fb_analysis:
	def __init__(self, token=None, user_id="me", graph=None, profile=None):
		self.token = token
		self.user_id = user_id
		self.graph =graph
		self.profile = profile
		
		
	def init_fb(self):
		self.graph = facebook.GraphAPI(self.token)
		self.profile = self.graph.get_object(self.user_id)
	
	def get_message_content(self):
		feed = self.graph.get_object('/me/feed', limit=1)
		print feed
        
		
		
if __name__ == "__main__":
	fb_obj = fb_analysis(token="CAACEdEose0cBAGZAqS39B1qNTrV9UtAG6LWCitF6xiEowoyFVvtjNTUwkzcO2Mv57yQcqaDCBFxvPs6Sr3RHZCcARpXtazbBraxkcO6oYR4ZC4by4rrWmPtWd5lxYsmPaW3VJlJauLQhd6Q9YmcDvEY1uLjNMcn1ugvgn47CYvmKp4RLGQ3ZBYaocBeijMFeRJlDEZBiubGl2J9GkEELl", user_id="100000101657890")
	
	fb_obj.init_fb()
	
	fb_obj.get_message_content()