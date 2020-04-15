#! venv/bin/python

import os
import pandas as pd
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def get_data(username):
    with open('keys.json', 'r') as f:
        keys = json.loads(f.read())

    CLIENT_ID = keys['client_id']
    CLIENT_SECRET = keys['client_secret']

    client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID,
                                                        client_secret=CLIENT_SECRET)

    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def parse_track_info(track):
        t_id = track['id']
        name = track['name']
        artist = track['artists'][0]['name']
        return {'name': name,
                'artist': artist,
                'id': t_id}

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

    key_features = ['danceability',
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
                    'time_signature'
                    ]

    def get_features(row):
        audio_features = sp.audio_features(row['id'])[0]
        for f in key_features:
            row[f] = audio_features[f]
        return row

    df = df.apply(get_features, axis=1)
    return df.to_dict(orient='records')

