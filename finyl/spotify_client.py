import requests

from finyl.settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET


SPOTIFY_URL = 'https://api.spotify.com/'
SPOTIFY_ACCOUNTS_URL = 'https://accounts.spotify.com/api/'


class SpotifyClient():
    """Spotify client class"""

    def __init__(self):
        self.token = self.get_token()
        self.headers = {
            "Authorization": f"Bearer {self.token}"
        }

    def get_token(self) -> str:
        """get spotify bearer authentication"""
        data = {
            "grant_type": "client_credentials",
            "client_id": SPOTIFY_CLIENT_ID,
            "client_secret": SPOTIFY_CLIENT_SECRET
        }
        try:
            response = requests.post(SPOTIFY_ACCOUNTS_URL + "token", data=data)
            response.raise_for_status()
        except requests.HTTPError as e:
            print(e)

        response = response.json()
        return response.get("access_token")

    def get_album(self, id: str) -> dict:
        """get album info"""
        try:
            response = requests.get(
                f"{SPOTIFY_URL}v1/albums/{id}",
                headers = self.headers
            )
            response.raise_for_status()
        except requests.HTTPError as e:
            print(e)

        response = response.json()
        return response

    def play_album(self, id: str) -> dict:
        """play album"""
        data = {
            "context_uri": f"spotify:album:{id}",
            "position_ms": 0
        }
        try:
            response = requests.put(
                f"{SPOTIFY_URL}v1/me/player/play/",
                headers = self.headers,
                data=data
            )
            response.raise_for_status()
        except requests.HTTPError as e:
            print(e)

        response = response.json()
        return response