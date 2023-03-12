import requests
from json import JSONDecodeError
from flask import Blueprint, jsonify, request


album_bp = Blueprint('album-info', __name__)
artist_id_by_name = {
    'Coldplay': 111239,
    'Miley Cyrus': 113672,
    'The Weeknd': 112024,
    'Lady Gaga': 111236,
    'Rihanna': 111305,
    'Justin Bieber': 111626,
    'Imagine Dragons': 114415,
    'Drake': 111718,
    'Beyoncé': 114364,
    'Madonna': 111255}

def get_artist_id_and_name(
        artist: str = 'coldplay'
    ) -> tuple[str]:
    url_artist = f'https://www.theaudiodb.com/api/v1/json/2/search.php?s={artist}'
    res = requests.get(url_artist).json()
    artist = res['artists'][0]
    artist_id = artist['idArtist']
    artist_name = artist['strArtist']
    return artist_id, artist_name


def get_albums_by_artist_id(
        artist_id: str = 111239, # 111239; 112024
    ) -> list[dict]:
    url_disc = f'https://theaudiodb.com/api/v1/json/2/album.php?i={artist_id}' # 111239; 112024
    res = requests.get(url_disc).json()
    albums = list()
    for album in res['album']:
        alb = dict()
        alb['strAlbum'] = album['strAlbum']
        alb['idAlbum'] = album['idAlbum'] # '2386593'
        alb['intYearReleased'] = album['intYearReleased']
        albums.append(alb)
    return albums


def get_discography_by_artist(
        artist: str = 'coldplay'
    ) -> list[dict]:
    url_disco = f'https://theaudiodb.com/api/v1/json/2/discography.php?s={artist}'
    res = requests.get(url_disco).json()
    discography = res['album']
    return discography


def get_tracks_by_album_id(
        album_id: str = 2115888
    ) -> list[dict]:
    url_tracks = f'https://theaudiodb.com/api/v1/json/2/track.php?m={album_id}'
    res = requests.get(url_tracks).json()
    tracks = {i+1: track['strTrack']
                for i, track in enumerate(res['track'])}
    return tracks


def get_artist_last_album(artist):
    artist_id, artist_name = get_artist_id_and_name(artist)
    discography = get_discography_by_artist(artist)
    latest_album = discography[0]['strAlbum']
    albums = get_albums_by_artist_id(artist_id)
    for album in albums:
        if album['strAlbum'] == latest_album:
            album_id = album['idAlbum']
            album_year = album['intYearReleased']
            break
    tracks = get_tracks_by_album_id(album_id)
    data = {
        'artist-id': artist_id,
        'artist': artist_name,
        'latest-album': latest_album,
        'latest-album-id': album_id,
        'album-year': album_year,
        'album-tracks': tracks}
    return data


@album_bp.route('/album-info', methods=['GET'])
def album_info():
    artist = request.args.get('artist')
    if not artist:
        return jsonify({'error': 'Missing artist parameter'}), 400
    try: 
        data = get_artist_last_album(artist)
    except JSONDecodeError:
        return jsonify({'error': 'Error in finding discography of this artist'}), 400
    return jsonify(data), 200

