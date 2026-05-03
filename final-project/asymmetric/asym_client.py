import socket
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.fernet import Fernet

with socket.socket() as s:
    s.connect(('127.0.0.1', 5001))
    pub_bytes = s.recv(4096)
    public_key = serialization.load_pem_public_key(pub_bytes)

    session_key = Fernet.generate_key()
    enc_key = public_key.encrypt(
        session_key,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                     algorithm=hashes.SHA256(), label=None)
    )
    s.send(enc_key)

    cipher = Fernet(session_key)
    enc_msg = cipher.encrypt(b"Hello World")
    s.send(enc_msg)