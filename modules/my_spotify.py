# imports
import pandas as pd
import requests

print("start")

# variables
auth_url = 'https://accounts.spotify.com/api/token'
base_url = 'https://api.spotify.com/v1'


# function get_header: get authorization header
def get_header(client_id, client_secret):
    # generate token with a POST request
    auth_response = requests.post(auth_url, {'grant_type': 'client_credentials',
                                            'client_id': client_id,
                                            'client_secret': client_secret}).json()
    access_token = auth_response['access_token']
    auth_response
    header = {'Authorization': 'Bearer {token}'.format(token=access_token)}
    return header


# function get_artist: get info artist for a selected id artist
def get_artist(id_artist, header):
    resource = '/artists'
    parameters = f'/{id_artist}'
    url = base_url + resource + parameters
    response = requests.get(url, headers=header).json()
    dict_artist = dict((k, [response[k]]) for k in ['id', 'name'] if k in response)
    df_artist = pd.DataFrame(dict_artist)
    # rename columns
    df_artist = df_artist.rename(columns={'id': 'artist_id', 'name': 'artist_name'})
    return df_artist 

# function get_related_artist: get related artist for a selected id artist
def get_related_artist(df_artist, header):
    id_artist = df_artist['artist_id'][0]
    resource = '/artists'
    parameters = f'/{id_artist}/related-artists'
    url = base_url + resource + parameters
    response = requests.get(url, headers=header).json()
    df_related_artists = pd.DataFrame(response['artists'])[['id','name']]
    # rename columns
    df_related_artists = df_related_artists.rename(columns={'id': 'related_id', 'name': 'related_name'})
    # include in dataframe selected id artist 
    df_related_artists['artist_id'] = id_artist
    # join artist and related artist to merge info
    df_related_artists = pd.merge(df_related_artists, df_artist, on='artist_id')
    return df_related_artists

# function get_tracks: get tracks for an id artist
def get_tracks(id_artist, header):
    resource = '/artists'
    parameters = f'/{id_artist}/top-tracks?market=ES'
    url = base_url + resource + parameters
    response = requests.get(url, headers=header).json()
    df_tracks = pd.DataFrame(response['tracks'])[['id','href','name','uri']]
    # include in dataframe selected id artist 
    df_tracks['related_id'] = id_artist
    return df_tracks

# function get_related_tracks: get tracks for id related artist from a selected id artist
def get_related_tracks(df_related_artists, header):
    df_related_tracks = pd.DataFrame()
    for i in df_related_artists['related_id']:
        df_tracks = get_tracks(i, header)
        df_related_tracks = pd.concat([df_related_tracks, df_tracks])

    # rename columns
    df_related_tracks = df_related_tracks.rename(columns={'id': 'track_id', 'href': 'track_href', 'name': 'track_name', 'uri': 'track_uri'})
    # join related artist and track related artist to merge info
    df_related_tracks = pd.merge(df_related_tracks, df_related_artists, on='related_id')
    return df_related_tracks


print("end")