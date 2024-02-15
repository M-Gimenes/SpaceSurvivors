import requests
import json
import socket
import functools
from cryptograph import Cryptograph
import routes


class Request():
    def __init__(self, gameStateManager) -> None:
        self.gameStateManager = gameStateManager

        self.url_key = routes.url_key
        self.url_data = routes.url_data
        self.url_update = routes.url_update
        encrypted_key = self.get_encrypted_key()
        if encrypted_key:
            self.key = {"key-API": Cryptograph().decrypt(encrypted_key)}

    def has_internet(function):
        @functools.wraps(function)
        def wrapper(self, *args, **kwargs):
            try:
                socket.create_connection(("8.8.8.8", 53), timeout=5)
                return function(self, *args, **kwargs)
            except OSError:
                self.gameStateManager.set_state('offline')
                return False
        return wrapper

    @has_internet
    def get_encrypted_key(self):
        response = requests.get(url=self.url_key)
        if response.status_code == 200:
            return response.json().get("key")
        else:
            self.gameStateManager.set_state('offline')

    @has_internet
    def set_data(self, player_info):
        headers = {"Content-Type": "application/json",
                   "action": "set_data"}
        headers.update(self.key)
        response = requests.post(
            url=self.url_data, headers=headers, data=json.dumps(player_info))
        if response.status_code == 200:
            print(response.json())
            return response.json()['result']
        else:
            self.gameStateManager.set_state('offline')

    @has_internet
    def get_data(self):
        headers = {"action": "get_data"}
        headers.update(self.key)
        response = requests.get(url=self.url_data, headers=headers)
        if response.status_code == 200:
            return response.json()['data']
        else:
            self.gameStateManager.set_state('offline')

    @has_internet
    def get_version(self):
        headers = {"action": "get_version"}
        headers.update(self.key)
        response = requests.get(url=self.url_data, headers=headers)
        if response.status_code == 200:
            return response.json()['version']
        else:
            self.gameStateManager.set_state('offline')
            return None

    @has_internet
    def get_public_key(self):
        headers = {"action": "get_public_key"}
        headers.update(self.key)
        response = requests.get(url=self.url_data, headers=headers)
        if response.status_code == 200:
            return response.content
        else:
            self.gameStateManager.set_state('offline')
            return None

    @has_internet
    def get_signature(self, player_save):
        headers = {"Content-Type": "application/octet-stream",
                   "action": "get_signature"}
        headers.update(self.key)
        response = requests.post(
            url=self.url_data, headers=headers, data=player_save)
        if response.status_code == 200:
            return response.content
        else:
            self.gameStateManager.set_state('offline')
            return None

    @has_internet
    def download_update(self, destino):
        with requests.get(self.url_update, stream=True) as response:
            with open(destino, 'wb') as arquivo:
                for chunk in response.iter_content(chunk_size=128):
                    arquivo.write(chunk)
