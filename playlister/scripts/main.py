#run the main script
import requests
import re

from . import playlist_io as io
from . import http_request as request
from . import distributions as dist
from . import genre 

def calculate(purl):
    #map of all songs, key:song-id, value: dict of attributes
    songs = {}

    #holds average of all attributes
    attribute_avg = {"duration_ms":0, "key":0, "mode":0, "time_signature":0, 
                    "acousticness":0, "danceability":0, "energy":0, "instrumentalness":0, 
                    "liveness":0, "loudness":0, "speechiness":0, "valence":0, "tempo":0}
    
    #hold the average percentile of each attribute
    attribute_percentile = {}

    #holds the highest percentile songs in each respective category
    high_songs = {"duration_ms":["",0], "acousticness":["",0], "danceability":["",0], "energy":["",0], 
                        "instrumentalness":["",0], "liveness":["",0], "loudness":["",0], "speechiness":["",0], 
                        "valence":["",0], "tempo":["",0]}

    #holds the lowest percentile songs in each respective category
    low_songs = {"duration_ms":["",999], "acousticness":["",999], "danceability":["",999], "energy":["",999], 
                        "instrumentalness":["",999], "liveness":["",999], "loudness":["",999], "speechiness":["",999], 
                        "valence":["",999], "tempo":["",999]}

    #load or initialize all the distributions
    dist.init()
    genre.init()
        
    #get authorization token and playlist id from input
    token = request.get_token()
    
    playlist_id = io.get_playlist_id(purl)
    if(playlist_id == -1):
        return playlist_id

    #get the songs, then load in their features
    request.get_playlist_tracks(songs, token, playlist_id)
    request.get_song_features(songs, attribute_avg, token)

    #get percentiles for playlist as a whole and for individual songs
    dist.get_overall_percentile(attribute_avg, attribute_percentile)
    dist.calculate_extreme_songs(songs, high_songs, low_songs)

    sort = genre.find_best_match(attribute_percentile)

    #pretty print to terminal
    oput = io.basic_oput(attribute_avg, attribute_percentile)
    oput.extend(io.extreme_oput(high_songs,low_songs))
    oput.append(f"1st guess: {sort[0][0]}\n2nd guess: {sort[1][0]}\n3rd guess: {sort[2][0]}")
    return oput

if __name__ == "__main__":
    calculate()

