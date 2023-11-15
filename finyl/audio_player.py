
import os

from enum import Enum
from pydub import AudioSegment, playback


class State(Enum):
    READY = 1
    PLAYING = 2

class Player:

    def __init__(self):
        self.state = State.READY
        self.cur_audio = 1

    def play_audio(self, file_path):
        sound = AudioSegment.from_file(file_path)
        self.state = State.PLAYING
        playback.play(sound)
        self.state = State.READY

    def play_album(self, album):
        """play a whole playlist from directory"""
        while self.cur_audio <= album.playlist_items:
            cur = f"{album.playlist_path}/{self.cur_audio}.mp3"
            if os.path.exists(
                f"{album.playlist_path}/{self.cur_audio+1}.mp3"
                ) or self.cur_audio >= album.playlist_items: #TODO: fix s + 1 hack ...should be cur
                print(f"Now playing: {self.cur_audio}")
                self.play_audio(cur)
                self.cur_audio = self.cur_audio + 1
        self.cur_audio = 1 # reset
