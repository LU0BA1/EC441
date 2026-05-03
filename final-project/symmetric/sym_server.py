import socket
from cryptography.fernet import Fernet

key = Fernet.generate_key()          # 44-character base64 key
cipher = Fernet(key)

with socket.socket() as s:
    s.bind(('127.0.0.1', 5000))
    s.listen(1)
    conn, _ = s.accept()
    with conn:
        # 1. Send key IN PLAINTEXT
        conn.send(key)
        # 2. Send an encrypted message
        enc = cipher.encrypt(b"Hello World")
        conn.send(enc)