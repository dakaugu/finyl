
import os

from enum import Enum
from pydub import AudioSegment, playback
from pytube import Playlist


class State(Enum):
    READY = 1
    PLAYING = 2


class Player:

    def __init__(self):
        self.state = State.READY
        self.cur_audio = 1

    def play_audio(self, file_path, offset):
        sound = AudioSegment.from_file(file_path)
        if offset:
            sound = sound[-(sound.duration_seconds - offset) * 1000:]
        self.state = State.PLAYING
        playback.play(sound)
        self.state = State.READY

    def play_album(self, album: Playlist, track: int, offset: int) -> None:
        """play a whole playlist from directory"""
        print(f"Now playing: {album.playlist.title}")
        if track:
            self.cur_audio = track
        while self.cur_audio <= album.playlist_items:
            cur = f"{album.playlist_path}/{self.cur_audio}.mp3"
            if os.path.exists(
                f"{album.playlist_path}/{self.cur_audio+1}.mp3"
                ) or self.cur_audio >= album.playlist_items: #TODO: fix s + 1 hack ...should be cur
                print(f"Now playing: {self.cur_audio}")
                self.play_audio(cur, offset)
                self.cur_audio = self.cur_audio + 1
                if offset:
                    offset = None # reset offset to start the next song from top
        self.cur_audio = 1 # reset

    def track_position():
        pass