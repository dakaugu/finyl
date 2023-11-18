import pytest
import os

from unittest.mock import Mock
from finyl.settings import DOWNLOAD_PATH
from finyl.yt_album import Album
from pydub import AudioSegment, playback


@pytest.fixture
def mock_get(mocker):
    mock = Mock()
    mocker.patch("finyl.yt_album.Album.get", return_value=mock)
    return mock


def test_album_has_playlist_info(mock_get):
    """Tests basic information from getting album"""
    mock_get.return_value = None
    album = Album("123")
    assert album.id == "123"
    assert album.playlist_path == f"{DOWNLOAD_PATH}{album.id}"
    assert album.playlist is None
    assert isinstance(album.playlist, type(None))


def test_audio():
    sound = AudioSegment.from_file(
        os.path.dirname(__file__) + "/../finyl/sounds/ping.mp3"
    )
    playback.play(sound)
