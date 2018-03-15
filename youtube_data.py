# youtube data
import json
import requests
from collections import OrderedDict


class Youtube_data:
    def __init__(self):
        self.api_key= "your key"
        self.video_location = "https://www.youtube.com/watch?v="
        self.api_url = "https://www.googleapis.com/youtube/v3/"
        self.api_search = "search?key={}".format(self.api_key)
        self.api_video_info = "videos?key={}".format(self.api_key)
        self.options = {
            "videoDuration": ["any", "long", "medium", "short"],
            "order": ["date", "rating", "relevance", "title", "videoCount", "viewCount"]
        };
        self.lang = "en"

    # public functions
    def get_search_url(self, query):
        self.__set_up_search_url()
        self.__set_search_count(query) 
        self.__check_options(query)
        self.__add_topic(query)
        return self.api_url


    def get_video_info_url(self, video_id): 
        return "{}{}&part=contentDetails,statistics,snippet&id={}".format(
            self.api_url, self.api_video_info, video_id)

    def get_search_ids(self, json_info):
        ids = []
        for x in json_info['items']:
            ids.append( "{}".format(x['id']['videoId']))
        return ids

    def get_videos_info(self, ids):
        info = {}
        count = 1
        for x in ids:
            info[str(count)] = self.__pull_video_info(x)
            count += 1
        return info

    def sort(self, arg, info):
        likes = {}
        hold = {}

        for x in info:
            likes[info[x]['id']] = info[x]['statistics']['likeCount']
            hold[info[x]['id']] = info[x]

        umm = OrderedDict(sorted(likes.items(), key=lambda t: t[1]))
            
        count = len(umm)
        new_info = {}
        for x in umm:
            new_info[str(count)] = hold[x]
            count -= 1

        return new_info

    # private functions 

    def __pull_video_info(self,id):
        url = self.get_video_info_url(id)
        req = requests.get(url)
        req = req.json()
        return req["items"][0]

    def __set_search_count(self, query):
        if "maxResults" in query:
            if query['maxResults'] < 0 or  query['maxResults'] > 50:
                raise ValueError('maxResults: 0-50')
            self.api_url += "&maxResults={}".format(query["maxResults"])
            del query['maxResults']

    def __check_options(self, query):
        self.__check("videoDuration", query)
        self.__check("order", query)
        self.__check('relevance', query)

    def __set_up_search_url(self):
        self.api_url += self.api_search
        self.__add_parts()
        self.__add_type()
      
    def __check(self, option_name, query):
        if option_name in query:
            self.__check_options_or_add_to_url(option_name, query)
    
    def __check_options_or_add_to_url(self, option_name, query):
        if query[option_name] in self.options[option_name]:
            self.__add_to_url(option_name, query[option_name])
        else:
            raise ValueError('{} options: {}'.format(
                    option_name, '{}'.format(", ".join(map(str, self.options[option_name])))))

    def __add_to_url(self, option_name, option): 
        self.api_url += "&{}={}".format(option_name, option)
        self.__add_relevance_lang_to_url(option_name, option)

    def __add_relevance_lang_to_url(self, option_name, option):
        if option_name == "order" and option == "relevance":
            self.api_url += "&relevanceLanguage={}".format(self.lang) 
     
    def __add_topic(self, query):
        if "topic" in query:
            self.api_url += "&q={}".format(query['topic'])
        else:
            raise ValueError('topic is required')

    def __add_parts(self):
        self.api_url += "&part=snippet"

    def __add_type(self):
        self.api_url += "&type=video"


if __name__ == "__main__":
    unittest.main()
