#! venv/bin/python

import os
import pandas as pd
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
    
KEY_FEATURES = ['danceability',
                'energy',
                'key',
                'loudness',
                'mode',
                'speechiness',
                'acousticness',
                'instrumentalness',
                'liveness',
                'valence',
                'tempo',
                'duration_ms',
                'time_signature']

def get_client(): 
    with open('keys.json', 'r') as f:
        keys = json.loads(f.read())

    CLIENT_ID = keys['client_id']
    CLIENT_SECRET = keys['client_secret']

    client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID,
                                                        client_secret=CLIENT_SECRET)

    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
def parse_track_info(track):
    t_id = track['id']
    name = track['name']
    artist = track['artists'][0]['name']
    return {'name': name,
            'artist': artist,
            'id': t_id}

def get_track_metadata(sp, username):
    playlists = sp.user_playlists(username)
    tracks = []

    for p in playlists['items']:
        track_list = sp.playlist(p['id'], fields='tracks')['tracks']
        for item in track_list['items']:
            if item['track']:
                track_info = parse_track_info(item['track'])
                track_info['playlist'] = p['name']
                tracks.append(track_info)
    
    df = pd.DataFrame(tracks)
    df.dropna(subset=['id'], inplace=True)
    df.drop_duplicates(subset='id', inplace=True)
    return df

def extract_audio_features(row):
    audio_features = sp.audio_features(row['id'])[0]
    for f in key_features:
        row[f] = audio_features[f]
    return row

def get_tracks(username):
    if os.path.isfile(os.path.join('data', 'tracks.csv')):
        df = pd.read_csv(os.path.join('data', 'tracks.csv'))
        return df.to_dict(orient='records')
    
    sp = get_client()
    track_meta_df = get_track_metadata(sp, username)
    df = track_meta_df.apply(extract_audio_features, axis=1)
    df.to_csv(os.path.join('data', 'tracks.csv'), index=False)

    return df.to_dict(orient='records')

if __name__ == '__main__':
    get_tracks('dtaylor072')



