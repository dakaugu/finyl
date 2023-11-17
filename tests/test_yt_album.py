import pytest

from unittest.mock import Mock
from finyl.yt_album import Album, DOWNLLOAD_PATH


@pytest.fixture
def mock_get(mocker):
    mock = Mock()
    mocker.patch("finyl.yt_album.Album.get", return_value=mock)
    return mock


def test_album_has_playlist_info(mock_get):
    mock_get.return_value = None
    album = Album("123")
    assert album.id == "123"
    assert album.playlist_path == f"{DOWNLLOAD_PATH}{album.id}"
    assert album.playlist is None
    assert isinstance(album.playlist, type(None))
