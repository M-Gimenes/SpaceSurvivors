from cryptography.fernet import Fernet
from secret import KEY_MASTER


class Cryptograph():
    def __init__(self) -> None:
        self.key_master = KEY_MASTER

    def decrypt(self, encrypted_key):
        f = Fernet(self.key_master)
        return f.decrypt(encrypted_key).decode()
