import json
import os
import time
from enum import Enum

from pydub import AudioSegment, playback

from finyl import logger
from finyl.yt_album import Album


class State(Enum):
    READY = 1
    PLAYING = 2


class Player:
    def __init__(self, album: Album):
        self.state = State.READY
        self.cur_audio = 1
        self.album = album

    def download_status(self) -> dict:
        with open(self.album.metadata_path, "r") as f:
            return json.load(f)

    def play_audio(self, file_path: str, offset: int) -> None:
        # -nostdin allows us to play audio in the background
        sound = AudioSegment.from_file(file_path, parameters=["-nostdin"])
        if offset:
            sound = sound[-(sound.duration_seconds - offset) * 1000 :]
        self.state = State.PLAYING
        playback.play(sound)
        self.state = State.READY

    def play_album(self, track: int, offset: int) -> None:
        """play a whole playlist from directory"""
        title = self.album.playlist.title if self.album.playlist else "N/A (offline)"
        logger.info(f"Now playing: {title}")
        if not os.path.exists(self.album.playlist_path):
            logger.warning("No directory for this album. Nothing to play")
        if track:
            self.cur_audio = track
        while self.cur_audio <= self.album.playlist_items:
            if self.download_status().get(str(self.cur_audio), 0):
                cur = f"{self.album.playlist_path}/{self.cur_audio}.mp3"
                logger.info(f"Now playing: {self.cur_audio}")
                self.play_audio(cur, offset)
                self.cur_audio = self.cur_audio + 1
                if offset:
                    offset = 0  # reset offset to start the next song from top
            else:
                time.sleep(0.1)
        self.cur_audio = 1  # reset

    def track_position(self):
        pass
