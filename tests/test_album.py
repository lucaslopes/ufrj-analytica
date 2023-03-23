import json
import requests


localhost = 'http://localhost:5000/'


url = localhost + 'album-info' + '?artist='


def test_album_info(artist=None):
    if artist == None:
        artist = 'Coldplay'
    req = requests.get(url + artist)
    res = req.json()
    if (code := req.status_code) == 200:
        print(code, res)
    correct = {'album-tracks': {'1': 'Higher Power (acoustic version)'}, 'album-year': '2021', 'artist': 'Coldplay', 'artist-id': 111239, 'latest-album': 'Higher Power (acoustic version)', 'latest-album-id': '2386593'}
    assert res == correct


artists = [
    'Coldplay',
    'Miley Cyrus',
    'The Weeknd',
    'Lady Gaga',
    'Rihanna',
    'Justin Bieber',
    'Imagine Dragons',
    'Drake',
    'Beyoncé',
    'Madonna']


for artist in artists:
    req = requests.get(url + artist)
    res = req.json()
    json_string = json.dumps(res)
    if (code := req.status_code) == 200:
        print(f'{code=}, {artist=}')
        print(json_string, '\n'*3)


# req = test_album_info('coldplay')
# req_wrong = test_album_info('coldplays')