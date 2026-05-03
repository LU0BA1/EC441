# Week 11 — Lab
## Scapy Packet Crafting and Traceroute: Hands‑on with Network Tools

---

### Lab Overview

This lab uses Scapy, a Python packet manipulation library, to construct and send custom network packets. It implements three classic network diagnostic tools from scratch:

1. An ICMP Echo Request (a custom `ping`).
2. A TCP SYN probe to port 80 (a basic port scan).
3. A complete traceroute using TTL exhaustion.

All traffic is captured with Wireshark, and every observed field is mapped back to concepts from Lectures 13–22.

---

### Part A: ICMP Echo Request (Custom Ping)

**What the script does:**  
Build an `IP(dst="8.8.8.8") / ICMP()` packet and send it with `sr1()`. The reply provides reachability, round‑trip time, and the remaining TTL.

**Captured packets (Wireshark view):**

| Packet | Source → Destination | Info | Notes |
| 1 | 10.0.0.246 → 8.8.8.8 | Echo (ping) request, ttl=64 | (no response found) |
| 2 | 10.0.0.246 → 8.8.8.8 | Echo (ping) request, ttl=64 | (reply in 3) |
| 3 | 8.8.8.8 → 10.0.0.246 | Echo (ping) reply, ttl=114 | |

*Why two requests?*  
The second packet (2) is the one sent by Scapy; packet 1 is an additional, duplicate request possibly triggered by the OS or a background process. Only packet 2 received a reply, which is the one Scapy processed.

**Key observations:**
- The TTL outbound = 64, the default Scapy assigns (matching Linux defaults).
- The TTL in the reply = 114. Assuming the server’s initial TTL is 128, the return path took 14 hops. The forward path required only 11 hops (see traceroute)—asymmetric routing is common.
- ICMP type fields are 8 (request) and 0 (reply), as described in Lecture 17.

---

### Part B: TCP SYN Probe (Port 80)

**What the script does:**  
Craft `IP(dst="8.8.8.8") / TCP(dport=80, flags="S")` and send it. A SYN‑ACK indicates an open port; RST‑ACK indicates closed; no response indicates filtered.

**Captured packets:**

| Packet | Source → Destination | Info |
| 4 | 10.0.0.246 → 8.8.8.8 | 20 → 80 [SYN] Seq=0 Win=8192 |
| 5 | 10.0.0.246 → 8.8.8.8 | [TCP Retransmission] 20 → 80 [SYN] Seq=0 Win=8192 |

**Result:**  
No reply was received, and the retransmission confirms the probe was lost or ignored. **Port 80 is filtered**—the server does not respond to TCP connections on that port.

**Key observations:**
- The SYN packet shows flags = 0x02 (SYN), sequence number = 0.
- The absence of a reply demonstrates port‑scanning logic: silent drop = filtered.

---

### Part C: Traceroute (TTL Exhaustion)

**What the script does:**  
Send an ICMP Echo Request with increasing TTL values (1 to 15). Each router that decrements TTL to 0 should respond with an ICMP Time Exceeded message, revealing its IP. When TTL is sufficient to reach the destination, an Echo Reply is received.

**Captured packets (abridged):**

For TTL values 1 through 10, no Time Exceeded replies were seen. Starting with TTL 11, the destination replied directly:

| Packet | TTL | Info |
|--------|-----|------|
| 6‑7   | 1   | Requests, no reply |
| 8‑9   | 2   | Requests, no reply |
| …     | …   | … |
| 24‑25 | 10  | Requests, no reply |
| 26‑27 | 11  | Requests; packet 27 got a reply |
| 28    | –   | Echo (ping) reply from 8.8.8.8, ttl=114 |

**Interpretation:**  
Intermediate routers silently dropped the expired packets (ICMP filtering is common). Despite the lack of visible intermediate hops, the traceroute succeeded: at TTL 11 the packet reached `8.8.8.8`, and the destination replied with an Echo Reply.

**Key observations:**
- 11 hops to reach Google’s DNS.
- The absence of ICMP Time Exceeded messages illustrates that traceroute relies on routers voluntarily sending them; it is not a guaranteed path‑discovery protocol.
- The final reply TTL (114) corroborates the earlier ping TTL.

---

### Summary of Findings

| Tool/Test | What we proved | Lecture connections |
|-----------|----------------|---------------------|
| ICMP Echo (ping) | TTL, ICMP types, RTT estimation | L14, L17, L19 |
| TCP SYN probe | Port state detection (filtered) | L18, L19 |
| Traceroute | TTL exhaustion discovers destination; ICMP filtering hides intermediate routers | L13, L17 |

---

### Key Takeaways

- Scapy gives full control over every packet field, allowing anyone to recreate network diagnostic tools in a few lines of code.
- The TTL and ICMP mechanics studied in Lectures 13–17 are directly observable in live captures.
- TCP port scanning is straightforward with raw sockets: a single SYN packet reveals the state of a port.
- Real‑world traceroute is often incomplete due to ICMP filtering, yet the method still correctly identifies the destination when the TTL is sufficient.
- Working with live captures reinforces the layered protocol model—every crafted packet maps directly to the stack (Ethernet → IP → ICMP/TCP).

---

### Generative AI Usage

I used ChatGPT to assist with this lab:

- It suggested the Scapy script structure and explained how `sr1()` works.
- It helped interpret the Wireshark capture, pointing out the duplicate requests and the significance of the reply TTL.
