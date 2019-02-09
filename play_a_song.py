from urllib.request import Request, urlopen
from urllib.parse import urlencode
import json
import time
CLIENT_ID_64 = "ZGE1M2ExOTk3YWE5NDM3Y2JlYTU5ZGFmZWYyY2NjNmE6NjhkODk2YWE2ZDc3NGI2ZDg1OTEzNDdmODE4YzEwMGY="
REFRESH_TOKEN = 'AQDMlwPy2vH1rfW0NqItf5U97yFtCwXc-Tj9mRRppyp9xMzy190ch1CBKy-twlply58-l-TszZy3eqB4F5yRuVGrDYzTE6xlISWN49Qa6D5dMDPZHaPmTrahrRadRyH6TNWHlQ'
def request_access_token():
    url = 'https://accounts.spotify.com/api/token'
    parameters = {'grant_type' : 'refresh_token', 'refresh_token' : REFRESH_TOKEN}
    headers = { 'Authorization' : 'Basic ' + CLIENT_ID_64}
    data = urlencode(parameters).encode()
    request = Request(url, data, headers)
    response =  json.loads(urlopen(request).read())
    return response['access_token']

def search_tracks(query, access_token):
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
    request = Request(url,data, headers, method='PUT')
    urlopen(request)	
	
def im_feeling_lucky(song_query):
    access_token = request_access_token()
    search_result = search_tracks(song_query, access_token)
    if search_result:
        track = search_result[0]
        duration_ms = track['duration_ms']
        play_tracks([track['uri']], access_token)
        print()
        message = "Playing {} by {} from the album {}".format(track['name'], track['artists'][0]['name'], track['album']['name'])
    else:
        message = "No match found for " + song_query
    return message
	
if __name__ == "__main__":
    access_token = request_access_token()
    track_uris = []
    for i in range(5):
        query= input("Enter a song name: ")
        track = search_tracks(query, access_token)[0]
        album_name = track['album']['name']
        duration_ms = track['duration_ms']
        track_uris.append(track['uri'])
    play_tracks(track_uris,access_token)


