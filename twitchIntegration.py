import os
import json
import requests
import mySQLIntegration
from twitch import TwitchClient

# TWITCH AUTHENTICATION
client = TwitchClient('###############')
client_id = "##############"
client_secret = "###################"
oauth = "######################"
TWITCH_STREAM_API_ENDPOINT_V5 = "https://api.twitch.tv/helix/streams?"
API_HEADERS = {
    'Client-ID': client_id,
    'Accept': '#########################',
    'Authorization': "Bearer " + oauth
}

# RETURNS "live" IF A STREAMER IS LIVE, "notlive" IF THEY ARE NOT LIVE
def streamerstatus(streamer):
    params = {"user_login": streamer, "type": "live"}
    ittalkin = requests.get(TWITCH_STREAM_API_ENDPOINT_V5, params=params, headers=API_HEADERS)
    jsonthing = ittalkin.json()
    streams = jsonthing.get('data', [])
    if len(streams) > 0:
        return "live"
    else:
        return "notlive"
    

def searchstream(search):
    TWITCH_STREAM_API_ENDPOINT_V5 = f"https://api.twitch.tv/helix/search/channels?query={search}"
    params = {'limit':1, 'is_live':True}
    thingy = requests.get(TWITCH_STREAM_API_ENDPOINT_V5, params=params, headers=API_HEADERS)
    thinyjson = thingy.json()
    stream = thinyjson.get('data',[])[0]
    return stream.get('broadcaster_login')