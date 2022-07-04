from modules import my_spotify as spo


# variables
client_id = '' # CLIENT ID
client_secret = '' # CLIENT SECRET

id_selected = '1dfeR4HaWDbWqFHLkxsg1d'

url_data = 'data/my_related_tracks.csv'


def main():
    print('start')
    
    header = spo.get_header(client_id, client_secret)
    my_artist = spo.get_artist(id_selected, header)
    my_related_artists = spo.get_related_artist(my_artist, header)
    my_related_tracks = spo.get_related_tracks(my_related_artists, header)
    my_related_tracks.to_csv(url_data)
    
    print('end')
    

if __name__ == '__main__':
    main()
