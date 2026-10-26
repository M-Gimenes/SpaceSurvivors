import base64
import functools
import socket

import requests

import routes

TIMEOUT = 15


class Request():
    """Conversa com o servidor do jogo (rotas em routes.py, fora do git).

    Não existe chave de API: o jogador se identifica pelo token que recebe ao
    cadastrar o nick. O servidor decide se um score vale, então nada aqui é segredo.
    """

    def __init__(self, gameStateManager) -> None:
        self.gameStateManager = gameStateManager
        self.base = routes.BASE.rstrip('/')

    def online(function):
        """Sem internet ou sem resposta do servidor: vai para a tela offline e devolve None."""
        @functools.wraps(function)
        def wrapper(self, *args, **kwargs):
            try:
                socket.create_connection(("8.8.8.8", 53), timeout=5).close()
                return function(self, *args, **kwargs)
            except (OSError, ValueError):  # inclui erros do requests e JSON inválido
                self.gameStateManager.set_state('offline')
                return None
        return wrapper

    def _get(self, path, **kwargs):
        return requests.get(self.base + path, timeout=TIMEOUT, **kwargs)

    def _post(self, path, payload):
        return requests.post(self.base + path, json=payload, timeout=TIMEOUT)

    @online
    def get_version(self):
        response = self._get('/version')
        if response.status_code != 200:
            self.gameStateManager.set_state('offline')
            return None
        return response.json()['version']

    @online
    def get_data(self):
        response = self._get('/ranking')
        if response.status_code != 200:
            self.gameStateManager.set_state('offline')
            return None
        return response.json()['data']

    @online
    def register(self, nickname):
        """Cadastra o nick. Devolve (resultado, token): 1 aceito, 2 em uso, 3 inválido, 0 tente depois."""
        response = self._post('/register', {'nickname': nickname})
        if response.status_code != 200:
            return 0, None
        body = response.json()
        return body.get('result', 0), body.get('token')

    @online
    def claim(self, save_bytes, signature_bytes):
        """Migra um save da 1.0.0. Devolve o JSON do servidor, ou {} se ele não respondeu direito."""
        response = self._post('/claim', {
            'save': base64.b64encode(save_bytes).decode(),
            'signature': base64.b64encode(signature_bytes).decode(),
        })
        if response.status_code != 200:
            return {}
        return response.json()

    @online
    def start_run(self, nickname, token):
        """Avisa o servidor que a partida começou. Sem isso o score não é aceito."""
        return self._post('/run/start', {'nickname': nickname, 'token': token}).status_code == 200

    @online
    def finish_run(self, nickname, token, score):
        """Envia o score da partida. Devolve {'accepted', 'best'} ou None se não valeu."""
        response = self._post('/run/finish', {'nickname': nickname, 'token': token, 'score': score})
        if response.status_code != 200:
            return None
        return response.json()

    @online
    def download_update(self, destino):
        with requests.get(self.base + '/download_update', stream=True, timeout=TIMEOUT) as response:
            response.raise_for_status()
            with open(destino, 'wb') as arquivo:
                for chunk in response.iter_content(chunk_size=65536):
                    arquivo.write(chunk)
        return True
