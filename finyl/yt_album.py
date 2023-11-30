import json
import os
from pytube import Playlist
from finyl.settings import YT_URI, DOWNLOAD_PATH


class Album:
    def __init__(self, id):
        self.id = id
        self.playlist_path = f"{DOWNLOAD_PATH}{id}"
        self.metadata_path = f"{DOWNLOAD_PATH}{id}/metadata.json"
        self.playlist = None
        self.get(id)
        self.download_status = {}

    def get(self, playlist_id: str) -> None:
        """Fetch playlist info"""
        self.playlist = Playlist(YT_URI + "playlist?list=" + playlist_id)
        if self.playlist:
            self.playlist_items = len(self.playlist)

    def update_track_download_status(self, track) -> None:
        """Update download status of a track
        1 -> downloaded
        0 -> not downloaded
        """
        self.download_status[track] = 1
        with open(self.metadata_path, "w") as f:
            json.dump(self.download_status, f)

    def download(self, overwrite=False) -> None:
        """Creates path download songs
        overwrite: ignore file existence and remove older files
        """
        print(f"{self.playlist_items} items to download")
        if not os.path.exists(self.playlist_path):
            os.mkdir(self.playlist_path)

        # create metadata file if it does not exist
        if not os.path.exists(self.metadata_path):
            with open(self.metadata_path, "w") as f:
                json.dump({}, f)

        if not self.playlist:
            self.playlist = Playlist(YT_URI + "playlist?list=" + self.id)

        if overwrite:  # TODO: TOBEDONE
            pass

        i = 1
        for video in self.playlist.videos:
            file_name = f"{self.playlist_path}/{i}.mp3"

            if os.path.exists(file_name) and not overwrite:
                # TODO: if file exists but status is not downloaded overwrite
                print(f"{file_name} already downloaded")
                self.update_track_download_status(i)
            else:
                video.streams.filter().get_audio_only().download(filename=file_name)
                self.update_track_download_status(i)
                print(f"{i} downloaded")
            i = i + 1
        print("Done!")
