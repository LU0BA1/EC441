from scapy.all import rdpcap, TCP, Raw
from cryptography.fernet import Fernet

pcap = rdpcap("../sym_capture.pcapng")

key = None
ciphertext = None

# Collect all payloads from server → client (source port 5000)
for pkt in pcap:
    if TCP in pkt and pkt[TCP].sport == 5000 and Raw in pkt:
        payload = bytes(pkt[TCP].payload)
        # The key is exactly 44 bytes (not starting with 'gAAAA')
        if len(payload) == 44:
            key = payload
            print(f"[+] Found key: {key.decode()}")
        # The ciphertext starts with 'gAAAA'
        elif payload.startswith(b'gAAAA'):
            ciphertext = payload
            print(f"[+] Found ciphertext (length {len(ciphertext)} bytes)")
            break

if key and ciphertext:
    cipher = Fernet(key)
    plaintext = cipher.decrypt(ciphertext)
    print(f"\n[!] DECRYPTED MESSAGE: {plaintext.decode()}")
else:
    print("[-] Could not extract key + ciphertext.")