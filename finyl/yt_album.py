import json
import os
from urllib.error import URLError

from pytube import Playlist

from finyl import logger
from finyl.settings import YT_URI, DOWNLOAD_PATH


class Album:
    def __init__(self, id: str):
        self.id = id
        self.playlist_path = f"{DOWNLOAD_PATH}{id}"
        self.metadata_path = f"{DOWNLOAD_PATH}{id}/metadata.json"
        self.playlist_items = 0
        self.playlist = self.get(id)
        self.download_status = {}

    def get(self, playlist_id: str) -> Playlist:
        """Fetch playlist info"""
        try:
            self.playlist = Playlist(YT_URI + "playlist?list=" + playlist_id)
            if self.playlist:
                self.playlist_items = len(self.playlist)
        except URLError as e:
            logger.error(e)
            self.playlist = None
            count = 0
            if os.path.exists(self.playlist_path):
                for file in os.listdir(self.playlist_path):
                    if file.endswith(".mp3"):
                        count += 1
                self.playlist_items = count
        return self.playlist

    def update_track_download_status(self, track: int) -> None:
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
        logger.info(f"{self.playlist_items} items to download")
        if not os.path.exists(self.playlist_path):
            os.mkdir(self.playlist_path)

        # create metadata file if it does not exist
        if not os.path.exists(self.metadata_path):
            with open(self.metadata_path, "w") as f:
                json.dump({}, f)

        if not self.playlist:
            return

        if overwrite:  # TODO: TOBEDONE
            pass

        for i, video in enumerate(self.playlist.videos, 1):
            file_name = f"{self.playlist_path}/{i}.mp3"

            if os.path.exists(file_name) and not overwrite:
                # TODO: if file exists but status is not downloaded overwrite
                logger.info(f"{file_name} already downloaded")
                self.update_track_download_status(i)
            else:
                video.streams.filter().get_audio_only().download(filename=file_name)
                self.update_track_download_status(i)
                logger.info(f"{i} downloaded")
        logger.info("Done!")
