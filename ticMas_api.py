import urllib2
import json
import string
from pprint import pprint


class TicMas_api:
    def __init__(self,urls = list()):
        self.urls = urls

    def init(self, value = None):
        self.value = value

    def get_SearchEvent_paths(self, keywords):
        print('https://app.ticketmaster.com/discovery/v1/events.json?keyword=' + keywords.strip() + '&apikey=aGxxaAbwugLhG4up2t5fHtAsah52bGHY')        #print("Entered Function")
        feed = urllib2.urlopen('https://app.ticketmaster.com/discovery/v1/events.json?keyword=' + keywords.strip() + '&apikey=aGxxaAbwugLhG4up2t5fHtAsah52bGHY').read()
        parsed = json.loads(feed)
        json_dump = json.dumps(parsed, indent=4,sort_keys=True)
        self.extract_url(json_dump)
        #self.extract_name(json_dump)
        #self.extract_category(json_dump)

    # def extract_category(self, json_obj):
    #     cat = list()
    #     category = list()
    #     flag = False

    #     for line in json_obj.splitlines():
    #         if "\"attraction\"" in line:
    #             flag = True
    #         if "url" in line and flag
    #             colon_index = line.find(":")
    #             extracted_categories = line[colon_index+2:].replace("\"","")
    #             cat.append(extracted_categories.replace(",",""))
    #             if "image" in line and flag
    #                 flag False     
    #             flag = False



    def extract_url(self, json_obj):
        for line in json_obj.splitlines():
            if "url" in line:
                print("found url"+line)
                colon_index = line.find(":")
                extract_url = line[colon_index+2:].replace("\"","")
                self.urls.append(extract_url)

    # def extract_name(self, json_obj):
    #     names = list()
    #     for line in json_obj.splitlines():
    #         if "name" in line:
    #             print("found name"+line)
    #             colon_index = line.find(":")
    #             extract_name = line[colon_index+2:].replace("\"","")
    #             names .append(extract_name)

    def write_url_file(self,filename):
        with open(filename,'w') as fout:
            for url in self.urls:
                fout.write(url + "\r\n") 

     # def write_cat_file(self,filename,lists):
     #    with open(filename,'wb') as fout:
     #        for url in cat:
     #            fout.write(url.strip()+"\r\n")            

if __name__ == "__main__":
    tm_obj = TicMas_api()
    tm_obj.init()

    tm_obj.get_SearchEvent_paths()
    tm_obj.write_url_file("TM_EvenUrl.txt")
    #tm_obj.write_url_file("TM_EvenName.txt","name",names)
    #tm_obj.write_cat_file("TM_Test".txt,cat)

