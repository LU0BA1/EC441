import socket
from cryptography.fernet import Fernet

with socket.socket() as s:
    s.connect(('127.0.0.1', 5000))
    key = s.recv(1024)                # receive key in plaintext
    cipher = Fernet(key)
    enc = s.recv(1024)
    print("Decrypted:", cipher.decrypt(enc).decode())