import os
import sys

import spotipy
from pytube import Search
from spotipy.oauth2 import SpotifyClientCredentials


class SpotipyAlbum:
    def __init__(
        self,
        name: str,
        images: list[str],
        release_date: str,
    ) -> None:
        self.name = name
        self.images = images
        self.release_year = int(release_date.split('-')[0])


class SpotipySong:
    def __init__(self, name: str, artists: list, album: dict, duration_ms: int) -> None:
        self.name = name
        self.artists = [artist['name'] for artist in artists]
        self.album = SpotipyAlbum(
            album['name'],
            album['images'],
            album['release_date'],
        )
        self.duration_ms = duration_ms


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
        playlist_uri = url.split('/')[-1].split('?')[0]
        track_uris = [
            x['track']['uri']
            for x in self.client.playlist_tracks(playlist_uri)['items']
        ]
        for track_uri in track_uris:
            self.process_song(track_uri)

    def process_song(self, url: str) -> None:
        self.get_sp_song(url)

    def get_sp_song(self, url):
        song = self.client.track(url)
        print(song['name'])
        sp_song = SpotipySong(
            song['name'],
            song['artists'],
            song['album'],
            song['duration_ms'],
        )
        self.download_yt_song(sp_song)

    def download_yt_song(self, sp_song: SpotipySong):
        print(sp_song.name)
        res = Search(sp_song.name)
        print(res.results)
