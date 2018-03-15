# test cases

import unittest
from youtube_data import Youtube_data

class Test_Youtube_Data(unittest.TestCase):

    def setUp(self):
        self.youtube_data = Youtube_data();
        self.youtube_key = "your key"


    def tearDown(self):
        pass

    def test_create_youtube_data_api_url_for_nba(self):
        url = self.youtube_data.get_search_url({"topic":"nba"})
        args = "key={}&part=snippet&type=video&q=nba".format(
            self.youtube_key) 
        self.assertEqual(url,"https://www.googleapis.com/youtube/v3/search?{}".format(args));
    
    def test_create_youtube_data_api_url_for_nfl(self):
        url = self.youtube_data.get_search_url({"topic":"nfl"})
        args =  "key={}&part=snippet&type=video&q=nfl".format(
            self.youtube_key) 
        self.assertEqual(url,"https://www.googleapis.com/youtube/v3/search?{}".format(args));

    def test_create_youtube_data_api_url_for_nfl_with_duration_error(self):
        with self.assertRaisesRegexp(ValueError, 'videoDuration options: any, long, medium, short'):
            self.youtube_data.get_search_url({"topic":"nfl", "videoDuration": "error"})
    
    def test_create_youtube_data_api_url_for_nfl_with_duration_valid(self):
        url = self.youtube_data.get_search_url({"topic":"nfl", "videoDuration": "any"})
        args = "key={}&part=snippet&type=video&videoDuration=any&q=nfl".\
            format(self.youtube_key) 
        self.assertEqual(url, "https://www.googleapis.com/youtube/v3/search?{}".format(args));

    def test_create_youtube_data_api_url_for_nfl_with_relevance_error(self):
         args = {
            "topic":"nfl",
            "videoDuration": "any",
            "order": "error"
        } 
         with self.assertRaisesRegexp(
                ValueError, 'order options: date, rating, relevance, title, videoCount, viewCount'):
            self.youtube_data.get_search_url(args)

    def test_create_youtube_data_api_url_for_nfl_with_relevance(self):
        url = self.youtube_data.get_search_url({
            "topic":"nfl", 
            "videoDuration": "any",
            "order": "relevance"})
        args = "key={}&part=snippet&type=video&videoDuration=any&order=relevance&relevanceLanguage=en&q=nfl".\
            format(self.youtube_key) 
        self.assertEqual(url, "https://www.googleapis.com/youtube/v3/search?{}".format(args));

    
    def test_create_youtube_data_url_with_one_count(self):
        url = self.youtube_data.get_search_url({
            "topic":"nfl", 
            "videoDuration": "any",
            "order": "relevance",
            "maxResults":1})
        args = "key={}&part=snippet&type=video&maxResults=1&videoDuration=".format(self.youtube_key)
        args  += "any&order=relevance&relevanceLanguage=en&q=nfl"
        self.assertEqual(url, "https://www.googleapis.com/youtube/v3/search?{}".format(args));


    def test_create_youtube_data_url_with_bad_count_min(self):    
        args = {
            "topic":"nfl",
            "videoDuration": "any",
            "maxResults":-1
        } 
        with self.assertRaisesRegexp(
                ValueError, 'maxResults: 0-50'):
            self.youtube_data.get_search_url(args)
    
    def test_create_youtube_data_url_with_bad_count_max(self):    
        args = {
            "topic":"nfl",
            "videoDuration": "any",
            "maxResults":51
        } 
        with self.assertRaisesRegexp(
                ValueError, 'maxResults: 0-50'):
            self.youtube_data.get_search_url(args)
         
    def test_get_video_info(self):
        info = self.youtube_data.get_video_info_url("sG4lZU1iPpE")
        self.assertEqual(
            info,
            "https://www.googleapis.com/youtube/v3/videos?key=AIzaSyBy7g1ogoE72VVlFwiBYVD2L-bOnASbZIk&part=contentDetails,statistics,snippet&id=sG4lZU1iPpE")
            
    
    def test_get_all_video_search_ids_in_search_of_one(self): 
        info = {
	     "kind": "youtube#searchListResponse",
	     "etag": "\"RmznBCICv9YtgWaaa_nWDIH1_GM/vP6psqbaIPtJ3qR2FwbQSxf-tM8\"",
	     "nextPageToken": "CAEQAA",
	     "regionCode": "US",
	     "pageInfo": {
	      "totalResults": 1000000,
	      "resultsPerPage": 1
	     },
	     "items": [
	      {
	       "kind": "youtube#searchResult",
	       "etag": "\"RmznBCICv9YtgWaaa_nWDIH1_GM/qXVbkIWu9eYn7006_6t77I5gXNg\"",
	       "id": {
		"kind": "youtube#video",
		"videoId": "sG4lZU1iPpE"
	       },
	       "snippet": {
		"publishedAt": "2018-03-14T16:55:36.000Z",
		"channelId": "UCuN9hYw2RpoAW8rZ3VK3isA",
		"title": "Harvick, NFL star Derek Carr talk Bakersfield food, weird kickers",
		"description": "NFL quarterback Derek Carr calls into Kevin Harvick's \"Happy Hours\" to talk about their favorite Mexican spots in their hometown of Bakersfield, Calif., as well as how kickers are a different breed.",
		"thumbnails": {
		 "default": {
		  "url": "https://i.ytimg.com/vi/sG4lZU1iPpE/default.jpg",
		  "width": 120,
		  "height": 90
		 },
		 "medium": {
		  "url": "https://i.ytimg.com/vi/sG4lZU1iPpE/mqdefault.jpg",
		  "width": 320,
		  "height": 180
		 },
		 "high": {
		  "url": "https://i.ytimg.com/vi/sG4lZU1iPpE/hqdefault.jpg",
		  "width": 480,
		  "height": 360
		 }
		},
		"channelTitle": "NASCAR",
		"liveBroadcastContent": "none"
	       }
	      }
	     ]
	    }  
        ids  = self.youtube_data.get_search_ids(info)
        self.assertEqual(['sG4lZU1iPpE'], ids) 


    def test_get_all_video_search_ids_in_search_of_two(self): 
    	info  = {
	     "kind": "youtube#searchListResponse",
	     "etag": "\"RmznBCICv9YtgWaaa_nWDIH1_GM/Jg87smEZmQshlZCeENhJW_W2VKU\"",
	     "nextPageToken": "CAIQAA",
	     "regionCode": "US",
	     "pageInfo": {
	      "totalResults": 1000000,
	      "resultsPerPage": 2
	     },
	     "items": [
	      {
	       "kind": "youtube#searchResult",
	       "etag": "\"RmznBCICv9YtgWaaa_nWDIH1_GM/qXVbkIWu9eYn7006_6t77I5gXNg\"",
	       "id": {
		"kind": "youtube#video",
		"videoId": "sG4lZU1iPpE"
	       },
	       "snippet": {
		"publishedAt": "2018-03-14T16:55:36.000Z",
		"channelId": "UCuN9hYw2RpoAW8rZ3VK3isA",
		"title": "Harvick, NFL star Derek Carr talk Bakersfield food, weird kickers",
		"description": "NFL quarterback Derek Carr calls into Kevin Harvick's \"Happy Hours\" to talk about their favorite Mexican spots in their hometown of Bakersfield, Calif., as well as how kickers are a different breed.",
		"thumbnails": {
		 "default": {
		  "url": "https://i.ytimg.com/vi/sG4lZU1iPpE/default.jpg",
		  "width": 120,
		  "height": 90
		 },
		 "medium": {
		  "url": "https://i.ytimg.com/vi/sG4lZU1iPpE/mqdefault.jpg",
		  "width": 320,
		  "height": 180
		 },
		 "high": {
		  "url": "https://i.ytimg.com/vi/sG4lZU1iPpE/hqdefault.jpg",
		  "width": 480,
		  "height": 360
		 }
		},
		"channelTitle": "NASCAR",
		"liveBroadcastContent": "none"
	       }
	      },
	      {
	       "kind": "youtube#searchResult",
	       "etag": "\"RmznBCICv9YtgWaaa_nWDIH1_GM/iFBhzb6xh79RIeyiFDwdYHOEAB0\"",
	       "id": {
		"kind": "youtube#video",
		"videoId": "MVQWfur6-qk"
	       },
	       "snippet": {
		"publishedAt": "2018-03-14T19:16:55.000Z",
		"channelId": "UCZ5C1HBPMEcCA1YGQmqj6Iw",
		"title": "Who's truly winning the NFL's Free Agency frenzy?",
		"description": "SportsPulse: The free agency frenzy in the NFL has been absolutely wild. Our experts pick the teams that are getting the most out the chaos. Read more: https://usat.ly/2tMZfCN Subscribe:...",
		"thumbnails": {
		 "default": {
		  "url": "https://i.ytimg.com/vi/MVQWfur6-qk/default.jpg",
		  "width": 120,
		  "height": 90
		 },
		 "medium": {
		  "url": "https://i.ytimg.com/vi/MVQWfur6-qk/mqdefault.jpg",
		  "width": 320,
		  "height": 180
		 },
		 "high": {
		  "url": "https://i.ytimg.com/vi/MVQWfur6-qk/hqdefault.jpg",
		  "width": 480,
		  "height": 360
		 }
		},
		"channelTitle": "USA TODAY Sports",
		"liveBroadcastContent": "none"
	       }
	      }
	     ]
	    }  
        ids  = self.youtube_data.get_search_ids(info)
        self.assertEqual(['sG4lZU1iPpE', "MVQWfur6-qk"], ids) 
	    
    def test_get_all_video_info_with_one_id(self): 
        info = self.youtube_data.get_videos_info(['sG4lZU1iPpE'])
        old_answer = { "1": {
   	        "kind": "youtube#video",
	        "etag": "\"RmznBCICv9YtgWaaa_nWDIH1_GM/kuRyQLUqMZJm-X08et6jENpmIxg\"",
	        "id": "sG4lZU1iPpE",
	        "snippet": {
		    "publishedAt": "2018-03-14T16:55:36.000Z",
		    "channelId": "UCuN9hYw2RpoAW8rZ3VK3isA",
		    "title": "Harvick, NFL star Derek Carr talk Bakersfield food, weird kickers",
		    "description": "NFL quarterback Derek Carr calls into Kevin Harvick's \"Happy Hours\" to talk about their favorite Mexican spots in their hometown of Bakersfield, Calif., as well as how kickers are a different breed.",
		    "thumbnails": {
		        "default": {
		            "url": "https://i.ytimg.com/vi/sG4lZU1iPpE/default.jpg",
		            "width": 120,
		            "height": 90
		        },
		        "medium": {
		            "url": "https://i.ytimg.com/vi/sG4lZU1iPpE/mqdefault.jpg",
		            "width": 320,
		            "height": 180
		        },
		        "high": {
		            "url": "https://i.ytimg.com/vi/sG4lZU1iPpE/hqdefault.jpg",
		            "width": 480,
		            "height": 360
		        },
		        "standard": {
		            "url": "https://i.ytimg.com/vi/sG4lZU1iPpE/sddefault.jpg",
		            "width": 640,
		            "height": 480
		        },
		        "maxres": {
		            "url": "https://i.ytimg.com/vi/sG4lZU1iPpE/maxresdefault.jpg",
		            "width": 1280,
		            "height": 720
		        }
		    },
		    "channelTitle": "NASCAR",
		    "categoryId": "17",
		    "liveBroadcastContent": "none",
		    "localized": {
		        "title": "Harvick, NFL star Derek Carr talk Bakersfield food, weird kickers",
		        "description": "NFL quarterback Derek Carr calls into Kevin Harvick's \"Happy Hours\" to talk about their favorite Mexican spots in their hometown of Bakersfield, Calif., as well as how kickers are a different breed."
		    },
		    "defaultAudioLanguage": "en-US"
	       },
	       "contentDetails": {
	            "duration": "PT1M15S",
		    "dimension": "2d",
		    "definition": "hd",
		    "caption": "false",
		    "licensedContent": "true",
		    "projection": "rectangular"
	       },
	       "statistics": {
		    "viewCount": "1610",
		    "likeCount": "55",
		    "dislikeCount": "2",
		    "favoriteCount": "0",
		    "commentCount": "7"
	       }
	      }
	    }
        # print "{}".format(info["1"])
        self.assertEqual(old_answer["1"]['id'], info["1"]["id"])
        
    def test_get_all_video_info_with_two_ids(self):
        info = self.youtube_data.get_videos_info(['sG4lZU1iPpE', 'MVQWfur6-qk'])
        self.assertEqual('sG4lZU1iPpE', info["1"]["id"])
        self.assertEqual('MVQWfur6-qk', info["2"]["id"])
              
    def test_get_all_video_likes_rank_1(self):
        info  = {
            "1": {
                "id": "sG4lZU1iPpE",
                "statistics":{
                    "likeCount":"6"
                }    
            },
            "2": {
                "id": "MVQWfur6-qk",
                "statistics":{
                    "likeCount":"2"
                }  
            }
        }
        rank = self.youtube_data.sort("likes",info);
        self.assertEqual('sG4lZU1iPpE', rank["1"]["id"])
        self.assertEqual('MVQWfur6-qk', rank["2"]["id"])

    
    def test_get_all_video_likes_rank_2(self):
        info  = {
            "1": {
                "id": "sG4lZU1iPpE",
                "statistics":{
                    "likeCount":"2"
                }    
            },
            "2": {
                "id": "MVQWfur6-qk",
                "statistics":{
                    "likeCount":"6"
                }  
            }
        }
        rank = self.youtube_data.sort("likes",info);
        self.assertEqual('sG4lZU1iPpE', rank["2"]["id"])
        self.assertEqual('MVQWfur6-qk', rank["1"]["id"])


if __name__ == "__main__":
    unittest.main()
