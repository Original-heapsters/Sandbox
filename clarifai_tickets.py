import os
import system
import fb_analysis as fb
import html_writer as html
import ticMas_api as tickets
import clarifai_comm as clarifai


class clarifai_tickets:


if __name__ == '__main__':
config_file = "config.json"
#Initialize all necessary classes
fb_obj = fb(config=config_file)
html_obj = html(config=config_file)
clarify_obj = clarifai(config=config_file)
ticket_obj = tickets(config=config_file)

#FB Operations
fb_obj.init_fb()
img_urls = fb_obj.get_image_paths()
messages = fb_obj.get_message_contents()
locations = fb_obj.get_location_paths()

# Tag Operations
tags = list()
location = list()
clarify_obj.get_fb_photo_tags(img_urls)
clarify_obj.get_fb_word_tags(messages)
location = clarify_obj.get_fb_recent_loc(locations)
clarify_obj.sort_all_tags()
tags = clarify_obj.get_filtered_keywords(4,11)

#Ticketmaster Operations
standard_events = ticket_obj.get_events()
relavant_events = ticket_obj.get_events(location, tags)

#Html Operations
html.write_html(standard_events,"standard.html")
html.write_html(relavant_events,"relavant.html")
print "done"
