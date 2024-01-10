import os
import sys

import spotipy
from pytube import Search
from spotipy.oauth2 import SpotifyClientCredentials


class SpotipySong:
    def __init__(self, song: dict) -> None:
        self.name = song['name']
        self.duration_ms = song['duration_ms']
        self.artists = [artist['name'] for artist in song['artists']]
        self.track_no = song['disc_number']
        self.album = self.SpotipyAlbum(song['album'])

    class SpotipyAlbum:
        def __init__(self, album: dict) -> None:
            self.name = album['name']
            self.cover = album['images'][0]['url']
            self.release_year = album['release_date'].split('-')[0]
            self.total_tracks = album['total_tracks']

        def __repr__(self) -> str:
            return (
                f'album name: {self.name}\n'
                f'album cover: {self.cover}\n'
                f'album release_year: {self.release_year}\n'
                f'album total_tracks: {self.total_tracks}'
            )

    def __repr__(self) -> str:
        return (
            f'name: {self.name}\n'
            f'duration_ms: {self.duration_ms}\n'
            f'artists: {self.artists}\n'
            f'track_no: {self.track_no}\n'
            f'{self.album}'
        )


class Quartz:
    def __init__(self, out_dir: str) -> None:
        self.out_dir = out_dir
        self.__setup_client()

    def __setup_client(self) -> None:
        client_id, client_secret = (
            os.getenv('QUARTZ_CLIENT_ID'),
            os.getenv('QUARTZ_CLIENT_SECRET'),
        )
        if client_id is None or client_secret is None:
            # TODO: pretty print
            print('Set quartz info')
            sys.exit(0)
        client_credentials_manager = SpotifyClientCredentials(
            client_id=client_id, client_secret=client_secret
        )
        self.client = spotipy.Spotify(
            client_credentials_manager=client_credentials_manager
        )

    def process_playlist(self, url: str) -> None:
        pass

    def process_song(self, url: str) -> None:
        self.get_sp_song(url)
        pass

    def get_sp_song(self, url):
        sp_song = self.client.track(url)
        sp_song = SpotipySong(sp_song)
        self.download_yt_song(sp_song)

    def download_yt_song(self, sp_song):
        search_query = f'{sp_song.name} by {sp_song.artists[0]} {sp_song.album.name}'
        search_res = Search(search_query).results
        print(search_res)

        pass
