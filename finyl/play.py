import argparse

from multiprocessing import Process
from finyl.yt_album import Album
from finyl.audio_player import Player
from finyl.starter import initialize

PREFERENCES = {
    "vinyl_feel": 0
}

if __name__ == "__main__":

    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument("playlist")
    arg_parser.add_argument("-track")
    arg_parser.add_argument("-offset")

    args = arg_parser.parse_args()
    print(args.playlist)
    track = int(args.track) if args.track else None
    offset = int(args.offset) if args.offset else None

    initialize(PREFERENCES)

    album = Album(args.playlist)
    p = Process(target=album.download, args=())
    p.start()
    print("downloading album")
    player = Player()
    player.play_album(album, track, offset)
