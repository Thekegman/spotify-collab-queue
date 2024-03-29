import urllib
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from threading import Thread, Event
import queue
import json
import time

CLIENT_ID_64 = "ZGE1M2ExOTk3YWE5NDM3Y2JlYTU5ZGFmZWYyY2NjNmE6NjhkODk2YWE2ZDc3NGI2ZDg1OTEzNDdmODE4YzEwMGY="
REFRESH_TOKEN = 'AQDMlwPy2vH1rfW0NqItf5U97yFtCwXc-Tj9mRRppyp9xMzy190ch1CBKy-twlply58-l-TszZy3eqB4F5yRuVGrDYzTE6xlISWN49Qa6D5dMDPZHaPmTrahrRadRyH6TNWHlQ'

FORBIDDEN_ARTISTS = ['smash mouth', 'ariana grande']

def request_access_token():
    url = 'https://accounts.spotify.com/api/token'
    parameters = {'grant_type' : 'refresh_token', 'refresh_token' : REFRESH_TOKEN}
    headers = { 'Authorization' : 'Basic ' + CLIENT_ID_64}
    data = urlencode(parameters).encode()
    request = Request(url, data, headers)
    response =  json.loads(urlopen(request).read())
    return response['access_token']

def search_track(query, access_token):
    url = 'https://api.spotify.com/v1/search'
    headers = {'Authorization': 'Bearer '+access_token}
    parameters = {'q' : query, 'type': 'track'}
    data = urlencode(parameters)
    
    request = Request(url+'?'+data, None, headers)
    response = json.loads(urlopen(request).read())
    if not response['tracks']['items']:
        print("Error: Artist Not Found")
        return None

    return response['tracks']['items'] 

def play_tracks(track_uris, access_token):
    url = 'https://api.spotify.com/v1/me/player/play'
    parameters = {'uris':track_uris}
    headers = {'Authorization': 'Bearer '+access_token}
    data = json.dumps(parameters).encode()
    print(url,data,headers,"PUT")
    request = Request(url,data, headers, method='PUT')
    try:
        print(urlopen(request).read())
    except urllib.error.URLError as e:
        print(e.reason)
    
	
def im_feeling_lucky(song_query):
    access_token = request_access_token()
    search_result = search_track(song_query, access_token)
    if search_result:
        track = search_result[0]
        duration_ms = track['duration_ms']
        play_tracks([track['uri']], access_token)
        message = "Playing {} by {} from the album {}".format(track['name'], track['artists'][0]['name'], track['album']['name'])
    else:
        message = "No match found for " + song_query
    return message

class MusicQueue:
    def __init__(self):
        self.track_queue = queue.Queue()
        self.track_history = []
        self.skip_sleep = Event()
        self.running_ind = 0
        
        self.queue_dispatcher = Thread(target=self.run, args=(int(self.running_ind),))
        self.queue_dispatcher.start()

    def drop(self, track_obj):
        with self.track_queue.mutex:
            try:
                self.track_queue.queue.remove(track_obj)
                return True
            except ValueError as e:
                print(e)
                return False
        
    def get_queue(self):
        print("get_Queue enter")
        with self.track_queue.mutex:
            track_list = list(self.track_queue.queue)
        print("get_Queue exit")
        return track_list
        
    def clear(self):
            print("clear enter")
            with self.track_queue.mutex:
                self.track_queue.queue.clear()
            self.skip_sleep.set()
            print("clear exit")
            
    def skip(self):
            print("skip enter")
            self.skip_sleep.set()
            print("skip exit")
            
    def add(self, song_query):
        access_token = request_access_token()
        search_result = search_track(song_query, access_token)
        track = None
        if search_result:
            track = search_result[0]
            track['timestamp'] = time.time()
            if track['artists'][0]['name'].lower() in FORBIDDEN_ARTISTS and False:
                message = "That artist is strictly forbidden"
            else:
                self.track_queue.put(track)
                self.track_history.append(track)
                message = "Track: {}\nArtist: {}\nAlbum: {}".format(track['name'], track['artists'][0]['name'], track['album']['name'])
        else:
            message = "No match found for " + song_query
        return (message, track)     

    def run(self, ind):
        while True:
            track_uris = []
            print("getting from queue")
            track = self.track_queue.get()
            self.skip_sleep.clear()
            print("got from queue")
            track_duration_sec = track['duration_ms']/1000.0
            track_uris.append(track['uri'])
            print("pushing: " +track['name'])
            access_token = request_access_token()
            play_tracks(track_uris, access_token)
            t1 = time.perf_counter()
            elapsed = 0
            print("entering sleep")
            print("skipped: ",self.skip_sleep.wait(track_duration_sec))
            

         
if __name__ == "__main__":
    access_token = request_access_token()
    track_uris = []
    for i in range(5):
        query= input("Enter a song name: ")
        track = search_track(query, access_token)[0]
        album_name = track['album']['name']
        duration_ms = track['duration_ms']
        track_uris.append(track['uri'])
    play_tracks(track_uris,access_token)


