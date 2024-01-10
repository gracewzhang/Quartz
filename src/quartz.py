import os
import shutil
import sys
import time

import ffmpeg
import music_tag
import spotipy
import wget
from pytube import Search
from rich.console import Console
from rich.prompt import Prompt
from spotipy.oauth2 import SpotifyClientCredentials

from utils import Color, ms_to_timestamp

cli = Console()


class SpotipySong:
    def __init__(self, song: dict) -> None:
        self.name = song['name']
        self.duration_ms = song['duration_ms']
        self.artist = ', '.join([artist['name'] for artist in song['artists']])
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
            f'artist: {self.artist}\n'
            f'track_no: {self.track_no}\n'
            f'{self.album}'
        )


class Quartz:
    def __init__(self, out_dir: str) -> None:
        self.out_dir = out_dir
        self.temp_dir = './temp/'
        self.__setup_client()

    def __setup_client(self) -> None:
        client_id, client_secret = (
            os.getenv('QUARTZ_CLIENT_ID'),
            os.getenv('QUARTZ_CLIENT_SECRET'),
        )
        if client_id is None or client_secret is None:
            cli.print(f'{Color.ERROR.value}Set quartz client ID & secret')
            sys.exit(0)
        client_credentials_manager = SpotifyClientCredentials(
            client_id=client_id, client_secret=client_secret
        )
        self.client = spotipy.Spotify(
            client_credentials_manager=client_credentials_manager
        )

    def playlist(self, url: str) -> None:
        sp_playlist = self.client.playlist(url)
        tracks = sp_playlist['tracks']['items']
        for idx, track in enumerate(tracks):
            sp_song = SpotipySong(track['track'])
            self.process_song(sp_song, idx + 1, len(tracks))

    def song(self, url: str) -> None:
        sp_song = self.get_sp_song(url)
        self.process_song(sp_song, 1, 1)

    def process_song(self, sp_song: SpotipySong, idx: int, total: int) -> None:
        cli.print(f'{Color.SUCCESS.value}Processing {idx}/{total}')
        downloaded_yt_path = self.download_yt_song(sp_song)
        m4a_path = self.trim_and_convert(downloaded_yt_path, sp_song)
        self.tag_m4a_file(m4a_path, sp_song)
        shutil.rmtree(self.temp_dir)
        cli.print(f'\n{Color.SUCCESS.value}Successfully saved {m4a_path}')

    def get_sp_song(self, url: str) -> SpotipySong:
        sp_song = self.client.track(url)
        sp_song = SpotipySong(sp_song)
        return sp_song

    def download_yt_song(self, sp_song: SpotipySong) -> str:
        cli.print(f'{Color.SYSTEM.value}Downloading {sp_song.name}...')
        search_query = f'{sp_song.name} by {sp_song.artist} {sp_song.album.name}'
        yt_song = Search(search_query).results[0]
        streams = yt_song.streams.filter(only_audio=True, file_extension='mp4')
        stream = max(streams, key=lambda s: s.filesize)
        path = stream.download(
            skip_existing=False,
            output_path=self.temp_dir,
        )
        cli.print(f'{Color.SYSTEM.value}Preliminary file saved to {path}')
        return path

    def get_timestamp(
        self, get_start: bool, min_timestamp: str, max_timestamp: str
    ) -> str:
        while True:
            if get_start:
                timestamp = Prompt.ask(
                    f'{Color.SYSTEM.value}Enter start timestamp', default=min_timestamp
                )
            else:
                timestamp = Prompt.ask(
                    f'{Color.SYSTEM.value}Enter end timestamp', default=max_timestamp
                )
            try:
                time.strptime(timestamp, '%H:%M:%S')
                if not min_timestamp <= timestamp <= max_timestamp:
                    raise IndexError
                break
            except ValueError:
                cli.print(
                    f"{Color.ERROR.value}Enter a valid timestamp in the format 'hh:mm:ss'"
                )
            except IndexError:
                cli.print(
                    f'{Color.ERROR.value}Provided timestamp is not within the valid range'
                )
        return timestamp

    def trim_and_convert(self, in_path: str, sp_song: SpotipySong) -> str:
        out_path = self.out_dir + sp_song.artist + ' - ' + sp_song.name + '.m4a'
        if not os.path.exists(self.out_dir):
            os.mkdir(self.out_dir)

        max_timestamp = ms_to_timestamp(sp_song.duration_ms)
        start_time = self.get_timestamp(True, '00:00:00', max_timestamp)
        end_time = self.get_timestamp(False, start_time, max_timestamp)

        cli.print(f'{Color.SYSTEM.value}Trimming and converting to m4a...')
        ffmpeg.input(in_path).output(
            out_path, ss=start_time, to=end_time, loglevel='quiet'
        ).run()
        return out_path

    def tag_m4a_file(self, path: str, sp_song: SpotipySong) -> None:
        cli.print(f'{Color.SYSTEM.value}Adding tags...')
        tags = music_tag.load_file(path)
        tags['tracktitle'] = sp_song.name
        tags['artist'] = sp_song.artist
        tags['album'] = sp_song.album.name
        tags['tracknumber'] = sp_song.track_no
        tags['totaltracks'] = sp_song.album.total_tracks
        tags['year'] = sp_song.album.release_year
        album_cover_path = self.download_album_cover(sp_song.album.cover, sp_song.name)
        with open(album_cover_path, 'rb') as img_in:
            tags['artwork'] = img_in.read()
        tags.save()

    def download_album_cover(self, cover_url: str, song_name: str) -> str:
        album_cover_path = self.temp_dir + song_name + '.png'
        wget.download(cover_url, out=album_cover_path)
        return album_cover_path
