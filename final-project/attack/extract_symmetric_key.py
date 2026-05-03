from scapy.all import rdpcap, TCP

pcap = rdpcap("symmetric/sym_capture.pcapng")
for pkt in pcap:
    if pkt.haslayer(TCP) and pkt[TCP].dport == 5000:
        payload = bytes(pkt[TCP].payload)
        if payload.startswith(b'gAAAA'):           # Fernet key starts with 'gAAAA'
            key = payload.strip()
            print("Stolen key:", key.decode())
            # Decrypt later message (hardcoded for demo)
            from cryptography.fernet import Fernet
            cipher = Fernet(key)
            # The second TCP segment in the capture is the encrypted msg
            # For demonstration, just show that we got the key
            break