import os
from multiprocessing import Process
from pydub import AudioSegment, playback


# TODO: move to preferences
def play_vinyl_crackle():
    """Play vinyl crackling in the background while playing records"""
    sound = AudioSegment.from_file(
        os.path.dirname(__file__) + "/sounds/vinyl_crackle.mp3"
    )
    sound = sound - 27  # -27db play it quieter than main audio
    playback.play(sound)
    play_vinyl_crackle()


def initialize(preferences):
    if preferences.get("vinyl_feel") == 1:
        p = Process(target=play_vinyl_crackle)
        p.start()
