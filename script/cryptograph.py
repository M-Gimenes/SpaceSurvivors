from cryptography.fernet import Fernet


class Cryptograph():
    def __init__(self) -> None:
        self.key_master = b'o_M54ZYEjvN0tjHl-MzHdN8PrptpQBdWEFBFBfRGDso='

    def decrypt(self, encrypted_key):
        f = Fernet(self.key_master)
        return f.decrypt(encrypted_key).decode()