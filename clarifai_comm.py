class clarifai_comm:
	def __init__(self,list_of_tags=list(),weighted_dict={}):
		self.list_of_tags = list_of_tags
		self.weighted_dict = weighted_dict
				
	def shorten_url(self, long_url):
		if len(argv) > 1:
			url = argv
			if len(argv) > 20:
				shortener = Shortener('TinyurlShortener')
				url = shortener.short(url.strip())
		else:
			print("ERROR")
			url = "http://www.clarifai.com/img/metro-north.jpg"
		return url
		
	def get_img_tags(self, url):
		returned_tags = list()
		command = 'curl -H "Authorization: Bearer b3A9PCVEzVkAijC1CC0qEUPNKcS9GE" --data-urlencode "url='
		command = command + url + '" https://api.clarifai.com/v1/tag/'
		command = command + " | python -mjson.tool > test.json"
		os.system(command)
		
		#Need desc
		with open('test.json') as test:
			data = json.load(test)

			#Prints tags to a file
		with open('tag.txt', 'w') as f:
			pprint(data['results'][0]['result']['tag']['classes'], f)
		
		#Reads file and appends all tags to a list
		with open('tag.txt', 'r') as f:
			for x in f:
				self.list_of_tags.append(x.split("'")[1]) 
				returned_tags.append(x.split("'")[1]) 
		return returned_tags
		
	def add_tags(self, more_tags=list()):
		for tag in more_tags:
			if self.weighted_dict.get(tag, "empty") == ("empty"):
				self.weighted_dict[tag] = 1
			else:
				self.weighted_dict[tag] += 1
				
	def get_fb_photo_tags(self,image_links=list()):
		#Method of getting urls.txt
		#Consider just passing in a list the is returned from fb_analysis
		## IMage Tags
		txtfile = sys.argv
		tags = []
		weight = dict();
		for url in image_links:
			img = shorten_url(url)
			tags.append(get_img_tags(img))

		add_tags(tags)
	
	def get_fb_word_tags(self,word_list=list()):
		## FB Word tags
		tags = []
		for x in word_list:
			tags.append(x.strip())
		add_tags(tags)
	
	def get_fb_recent_loc(self, locations=list())
		## FB Location
		location = []
		for x in locations:
			location.append(x.strip().split(",")[0].replace(" ","%20"))
		return location
		
	def sort_all_tags(self):
		self.weighted_dict = sorted(self.weighted_dict, key = self.weighted_dict.get, reverse = True)
	
	def get_filtered_keywords(self, min, max):
		key_words = list()
		
		for word in self.weighted_dict[min:max]:
			key_words.append(word[0])
		return key_words
	
	#Method of getting urls.txt
	#Consider just passing in a list the is returned from fb_analysis
	## IMage Tags
	txtfile = sys.argv
    tags = []
    weight = dict();
    with open(txtfile[1], 'r') as link:
        for x in link:
            img = shorten_url(x)
			get_img_tags(img)

    add_tags(tags)

	## FB Word tags
    tags = []
    with open('Words.txt', 'r') as txt:
        for x in txt:
            tags.append(x.strip())
    add_tags(weight,tags)
    
	## FB Location
    location = []
    with open('Location.txt', 'r') as txt:
        for x in txt:
            location.append(x.strip().split(",")[0].replace(" ","%20"))
	
	# Write sorted tag file
    with open('weightedTag.txt', 'w') as f:
        for w in sorted(weight, key = weight.get, reverse = True):
           f.write(w + "\n")

	#Only write the  top 7 results, offset by 4
    with open('weightedTag.txt', 'r') as f:
        with open('keywords.txt', 'w') as w:
            count = 0
            max_count = 11
            min_count = 4
            for line in f:
                if count in range(min_count, max_count):
                    w.write(location[0] + "," + line)
                count += 1

	#extraxt keywords into a list
    with open('keywords.txt', 'r') as f:
        kw = f.readline()

	#extract this into the calrifai tickets class
    tickets = ticMas_api.TicMas_api()
    tickets.get_SearchEvent_paths(kw)
    tickets.write_url_file("TM_EvenUrl.txt")

    #Put all links into a list
    ev_link = []
    with open("TM_EvenUrl.txt", 'r') as f:
        for line in f:
            ev_link.append(line)
    
	#Write the html to display the page
    html_writer.write_html(ev_link)				