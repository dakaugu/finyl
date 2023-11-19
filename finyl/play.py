import argparse

from multiprocessing import Process
from finyl.yt_album import Album
from finyl.audio_player import Player


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument("playlist")
    arg_parser.add_argument("-track")
    arg_parser.add_argument("-offset")

    args = arg_parser.parse_args()
    print(args.playlist)
    track = int(args.track) if args.track else 0
    offset = int(args.offset) if args.offset else 0

    album = Album(args.playlist)
    p = Process(target=album.download, args=())
    p.start()
    print("downloading album")
    player = Player()
    player.play_album(album, track, offset)
