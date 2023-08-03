from pathlib import Path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

KEY_FOLDER = ".config"
KEY_NAME = "key"


class KeyManagement:
    def __init__(self):
        if not self.__check_key_pair():
            self.__gen_key_pair()

        with open(Path(KEY_FOLDER, KEY_NAME), "rb") as f:
            self.private_key = Ed25519PrivateKey.from_private_bytes(f.read())

    def __check_key_pair(self):
        if not Path(KEY_FOLDER).exists():
            return False
        if not Path(KEY_FOLDER, KEY_NAME).exists():
            return False
        return True

    def __gen_key_pair(self):
        folder = Path(KEY_FOLDER)
        folder.mkdir(parents=True, exist_ok=True)

        # Gen key and save
        priv_key = Ed25519PrivateKey.generate()
        with open(folder / KEY_NAME, "wb") as f:
            f.write(
                priv_key.private_bytes(
                    encoding=serialization.Encoding.Raw,
                    format=serialization.PrivateFormat.Raw,
                    encryption_algorithm=serialization.NoEncryption(),
                )
            )

    def get_public_key(self):
        return self.private_key.public_key().public_bytes_raw()

    def sign(self, data):
        return self.private_key.sign(data)

    def verify(self, signature, data):
        return self.private_key.public_key().verify(signature, data)


if __name__ == "__main__":
    a = KeyManagement()
    print("[!] Check get public key:")
    print(a.get_public_key())
    print("-" * 100)
    print("[!] Check signing feature")
    msg = b"Hello world"
    sign = a.sign(msg)
    print(sign)
    print("-" * 100)
    print("[!] Verify signature")
    a.verify(sign, msg)
