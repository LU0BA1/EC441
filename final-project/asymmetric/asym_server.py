import socket
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.fernet import Fernet

private_key = rsa.generate_private_key(65537, 2048)
public_key = private_key.public_key()
pub_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

with socket.socket() as s:
    s.bind(('127.0.0.1', 5001))
    s.listen(1)
    conn, _ = s.accept()
    with conn:
        # 1. Send ONLY the public key
        conn.send(pub_bytes)
        # 2. Receive encrypted session key
        enc_key = conn.recv(1024)
        session_key = private_key.decrypt(
            enc_key,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                         algorithm=hashes.SHA256(), label=None)
        )
        # 3. Receive and decrypt message
        enc_msg = conn.recv(1024)
        cipher = Fernet(session_key)
        print("Decrypted:", cipher.decrypt(enc_msg).decode())