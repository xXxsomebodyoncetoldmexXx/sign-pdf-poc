from cryptography.hazmat.primitives.asymmetric import ed25519
from base64 import b64decode


def verify_pdf(signature, public_key, data):
    signature = b64decode(signature)
    public_key = ed25519.Ed25519PublicKey.from_public_bytes(b64decode(public_key))
    public_key.verify(signature, data)
