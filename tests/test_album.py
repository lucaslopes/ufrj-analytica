import requests
from utils import localhost


url = localhost + 'album-info' + '?artist='


def test_album_info(artist):
    req = requests.get(url + artist)
    print(req)
    if (code := req.status_code) == 200:
        print(code, req.json())
    return req

req = test_album_info('coldplay')
req_wrong = test_album_info('coldplays')

