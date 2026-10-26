import os
import pickle


class SaveManager():
    """Save local: nick, token, melhor score e idioma.

    Desde a 1.0.1 o recorde que vale é o do servidor; o save só lembra quem você é.
    O arquivo 'signature' é da 1.0.0 e serve apenas para migrar o nick (claim).
    """

    def __init__(self, request):
        game_data_dir = os.path.join(os.path.expanduser("~"), "SpaceSurvivors")
        os.makedirs(game_data_dir, exist_ok=True)
        self.save_archive = os.path.join(game_data_dir, 'save')
        self.signature_archive = os.path.join(game_data_dir, 'signature')
        self.request = request

    def load(self):
        try:
            with open(self.save_archive, 'rb') as archive:
                data = pickle.load(archive)
            return data if isinstance(data, dict) else {}
        except Exception:
            return {}

    def save(self, player_info):
        temp = self.save_archive + '.tmp'
        with open(temp, 'wb') as archive:
            pickle.dump(player_info, archive)
        os.replace(temp, self.save_archive)

    def change(self, key, value):
        aux = self.load()
        aux[key] = value
        self.save(aux)

    def migrate_legacy(self):
        """Prepara o save para jogar online.

        Devolve True se já tem nick e token, False se precisa escolher um nick (tela de
        login) e None se o servidor não respondeu (tenta de novo na próxima abertura).
        Um save da 1.0.0 tem nick mas não tem token: ele prova a posse com a assinatura
        antiga e recebe o token.
        """
        data = self.load()
        if not data.get('nickname'):
            return False
        if data.get('token'):
            return True
        try:
            with open(self.save_archive, 'rb') as archive:
                save_bytes = archive.read()
            with open(self.signature_archive, 'rb') as archive:
                signature = archive.read()
        except FileNotFoundError:
            signature = b''
        if signature:
            answer = self.request.claim(save_bytes, signature)
            if answer is None:
                return None
            result = answer.get('result')
            if result == 1:
                data['nickname'] = answer['nickname']
                data['token'] = answer['token']
                self.save(data)
                return True
            if result not in (2, 3):  # resposta inesperada: não apaga nada, tenta depois
                return None
        # O nick não pôde ser comprovado: escolhe outro, mantendo o idioma.
        data.pop('nickname', None)
        data.pop('score', None)
        self.save(data)
        return False
