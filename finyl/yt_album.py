import os
from pytube import Playlist
from finyl.settings import YT_URI, DOWNLOAD_PATH


class Album:
    def __init__(self, id):
        self.id = id
        self.playlist_path = f"{DOWNLOAD_PATH}{id}"
        self.playlist = None
        self.get(id)

    def get(self, playlist_id: str) -> None:
        """Fetch playlist info"""
        self.playlist = Playlist(YT_URI + "playlist?list=" + playlist_id)
        if self.playlist:
            self.playlist_items = len(self.playlist)

    def download(self, overwrite=False) -> None:
        """Creates path download songs
        overwrite: ignore file existence and remove older files
        """
        print(f"{self.playlist_items} items to download")
        if not os.path.exists(self.playlist_path):
            os.mkdir(self.playlist_path)

        if not self.playlist:
            self.playlist = Playlist(YT_URI + "playlist?list=" + self.id)

        if overwrite:  # TODO: TOBEDONE
            pass

        i = 1
        for video in self.playlist.videos:
            file_name = f"{self.playlist_path}/{i}.mp3"

            if os.path.exists(file_name) and not overwrite:
                print(f"{file_name} already downloaded")
            else:
                video.streams.filter().get_audio_only().download(filename=file_name)
                print(f"{i} downloaded")
            i = i + 1
