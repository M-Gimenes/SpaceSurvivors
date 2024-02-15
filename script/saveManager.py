import pickle
import os
import sys
import pygame as pg
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization


class SaveManager():
    def __init__(self, request):
        user_dir = os.path.expanduser("~")
        game_data_dir = os.path.join(user_dir, "SpaceSurvivors")
        if not os.path.exists(game_data_dir):
            os.makedirs(game_data_dir)
        self.save_archive = os.path.join(game_data_dir, 'save')
        self.signature_archive = os.path.join(game_data_dir, 'signature')
        self.request = request
        self.pem_key = self.request.get_public_key()
        self.public_key = None
        if self.pem_key:
            self.public_key = serialization.load_pem_public_key(self.pem_key)

    def load(self):
        try:
            with open(self.save_archive, 'rb') as archive1:
                player_info_bytes = archive1.read()
            with open(self.signature_archive, 'rb') as archive2:
                signature_bytes = archive2.read()
            if self.verify_signature(player_info_bytes, signature_bytes):
                with open(self.save_archive, 'rb') as archive:
                    data = pickle.load(archive)
                return data
            else:
                if self.public_key:
                    os.remove(self.save_archive)
                    os.remove(self.signature_archive)
                    pg.quit()
                    sys.exit()
                return {}
        except FileNotFoundError:
            return {}

    def save(self, player_info):
        signature = self.request.get_signature(pickle.dumps(player_info))
        if signature:
            with open(self.save_archive, 'wb') as archive:
                pickle.dump(player_info, archive)
            with open(self.signature_archive, 'wb') as archive:
                archive.write(signature)

    def verify_signature(self, file_content, signature):
        try:
            self.public_key.verify(
                signature,
                file_content,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception as e:
            print(f"Verification failed: {e}")
            return False

    def change(self, key, value):
        aux = self.load()
        aux[key] = value
        self.save(aux)
