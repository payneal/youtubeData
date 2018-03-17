# you tube data

## Requirements
### 1 get youtube web api key
* see https://www.slickremix.com/docs/get-api-key-for-youtube/

###  2 put key in ./src/youtube_data
* self.api_key = "key"

## Setup
### 3 get enviroment setup
* virtualenv venv
* source ./venv/bin/activate
* pip install -r requirements.txt

### run server
* python index.py

### api call example #1
* post localhost:8090/youtube_data
```json
    { 
        "topics": ["nba"],
        "filters":{
            "likes": "most"     
        }
    } 
```
* response ex
```json
    ["https://www.youtube.com/watch?v=KNHh60elNlY"]
```

### api call example #2 
* post localhost:8090/youtube_data
```json
    { 
        "topics": ["nba", "nfl"],
        "filters":{
            "likes": "most"     
        }
    } 
```
* response ex
```json
        [
            "https://www.youtube.com/watch?v=G8KkSDY0kTk", 
            "https://www.youtube.com/watch?v=8iEu2UGC9mA"
        ]
```


### how to use class youtube_data

```python

    import youtube_data from "location of youtube_data"

    youtube_data - Youtube_data();

    #  get a search url for a topic
    url = self.youtube_data.get_search_url({"topic":"nba"})
    
    #  more options used ex
    url = self.youtube_data.get_search_url({
        "topic":"nfl", 
        "videoDuration": "any",
        "order": "relevance",
        "maxResults":1})

    # get video url from video id
    url = self.youtube_data.get_video_info_url("sG4lZU1iPpE")
       

    # get video ids from json search result 
    ids  = self.youtube_data.get_search_ids(info)
    
    
    # get array of videoids  info 
    info = self.youtube_data.get_videos_info(['sG4lZU1iPpE', 'MVQWfur6-qk'])
       

    # sorting with most likes
    rank = self.youtube_data.sort("likes", "most", info);
     
    # look at ./src/test_youtube_data.py

```
