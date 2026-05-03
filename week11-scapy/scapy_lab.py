""" EC 441 Week 11 Lab: Scapy Packet Crafting, SYN probe, and Traceroute """

from scapy.all import IP, ICMP, TCP, sr1

DEST = "8.8.8.8"

print("[1] Crafting ICMP Echo Request ...")
pkt = IP(dst=DEST) / ICMP()
print("Packet structure:")
pkt.show() 

reply = sr1(pkt, timeout=2, verbose=0)
if reply:
    print(f"Reply from {reply.src}, TTL={reply.ttl}, type={reply.type}")
else:
    print("No reply (filtered?)")

print("\n[2] TCP SYN probe to port 80 ...")
syn = IP(dst=DEST) / TCP(dport=80, flags="S")
resp = sr1(syn, timeout=2, verbose=0)
if resp:
    if resp.haslayer(TCP) and resp[TCP].flags == 0x12:  # SYN+ACK
        print(f"Port 80 open at {resp.src}")
    elif resp.haslayer(TCP) and resp[TCP].flags == 0x14:  # RST+ACK
        print(f"Port 80 closed (RST)")
else:
    print("No response (filtered)")

print("\n[3] Traceroute ...")
for ttl in range(1, 16):
    probe = IP(dst=DEST, ttl=ttl) / ICMP()
    reply = sr1(probe, timeout=2, verbose=0)
    if reply is None:
        print(f"{ttl:2d}  *")
    elif reply.type == 0:
        print(f"{ttl:2d}  {reply.src} (reached)")
        break
    else:
        print(f"{ttl:2d}  {reply.src}")