# Week 7 — Problem Set
## Ethernet, ARP, and Switching: Worked Problems

---

### Problem 1: Ethernet Frame Fields

**Question:** An Ethernet frame arrives with the following fields (shown in order):  
Preamble/SFD (8 bytes), Destination MAC: `FF:FF:FF:FF:FF:FF`, Source MAC: `A4:C3:F0:12:34:56`, Type: `0x0806`, Payload: 28 bytes of data, FCS: 4 bytes.

(a) What is the total frame size in bytes?  
(b) Is this frame valid according to the Ethernet minimum frame size rule?  
(c) What upper-layer protocol is carried in this frame?  
(d) Who will process this frame — one device, a group of devices, or all devices on the LAN?  
(e) Why might the payload be padded, and if it is, how does the receiver know where the real data ends?

---

**Solution:**

**(a)** Total frame size including preamble/SFD:

| Field | Size |
|-------|------|
| Preamble/SFD | 8 bytes |
| Destination MAC | 6 bytes |
| Source MAC | 6 bytes |
| Type | 2 bytes |
| Payload | 28 bytes |
| FCS | 4 bytes |
| **Total** | **54 bytes** |

*Note:* The preamble/SFD is usually stripped by the NIC and not counted toward the frame size seen by the OS. The frame size **excluding** preamble/SFD is $54 - 8 = 46$ bytes. This is the number that matters for the minimum frame size check.

**(b)** The Ethernet minimum payload is 46 bytes (total frame without preamble = 64 bytes). Our frame has only 28 bytes of payload, so total = $6 + 6 + 2 + 28 + 4 = 46$ bytes. This is **below the 64-byte minimum**. In practice, the sender would **pad** the payload with 18 extra bytes to reach 46 bytes of payload, making the total frame 64 bytes. So as transmitted, the frame would be valid, but the 28 bytes reported here represent the real data, not the padded length.

**(c)** Type field `0x0806` corresponds to **ARP** (Address Resolution Protocol).

**(d)** Destination MAC `FF:FF:FF:FF:FF:FF` is the **broadcast address**. Every device on the LAN will receive and process this frame.

**(e)** The payload is padded because Ethernet requires a minimum of 46 bytes of payload (64 bytes total frame). The **Type/Length field** tells the receiver which protocol is inside, but it does **not** tell the receiver the payload length. That information comes from **inside the payload itself**:

- For IP (Type `0x0800`), the **IP Total Length field** tells the receiver exactly how many bytes are real data; the rest is padding.
- For ARP (Type `0x0806`), the ARP message itself has a fixed known size (28 bytes for IPv4 over Ethernet), so the receiver implicitly knows how much is real data.

The NIC does **not** strip the padding — the OS sees the padded frame and the IP/ARP layer ignores the extra bytes.

---

### Problem 2: ARP Exchange Trace

**Question:** Host A (IP: `192.168.1.10`, MAC: `AA:AA:AA:AA:AA:AA`) wants to send an IP datagram to Host B (IP: `192.168.1.20`). Host A's ARP table is empty.

Host B has MAC address `BB:BB:BB:BB:BB:BB`.

(a) What is the destination MAC address of the ARP request?  
(b) What is the destination MAC address of the ARP reply?  
(c) After the ARP exchange, what entry appears in Host A's ARP table?  
(d) After the ARP exchange, what entry (if any) appears in Host B's ARP table?  
(e) What would Host A do differently if Host B were on a different subnet (e.g., `10.0.0.5`)?

---

**Solution:**

**(a)** The ARP request is sent to the **broadcast** MAC address: `FF:FF:FF:FF:FF:FF`. This ensures every host on the LAN receives it.

**(b)** The ARP reply is **unicast** directly to Host A's MAC address: `AA:AA:AA:AA:AA:AA`. Only Host A needs the answer; there is no reason to broadcast it.

**(c)** Host A's ARP table will contain:

| IP Address | MAC Address |
|------------|-------------|
| 192.168.1.20 | BB:BB:BB:BB:BB:BB |

This entry will have a TTL (typically ~20 minutes).

**(d)** Host B learns Host A's mapping from the **ARP request itself** (the request contains the sender's IP and MAC). So Host B's ARP table will contain:

| IP Address | MAC Address |
|------------|-------------|
| 192.168.1.10 | AA:AA:AA:AA:AA:AA |

This is called **gratuitous learning** — every host on the LAN can update its cache from ARP requests it overhears.

**(e)** If Host B's IP were `10.0.0.5` (different subnet), Host A would:

1. Check its routing table and find that `10.0.0.5` is not on the local subnet.
2. Determine that the next hop is the **default gateway** (e.g., `192.168.1.1`).
3. **ARP for the gateway's MAC address**, not Host B's MAC address.
4. Encapsulate the IP datagram (destination IP still `10.0.0.5`) in an Ethernet frame addressed to the **gateway's MAC**.
5. The router receives the frame, strips the Ethernet header, looks up the route to `10.0.0.5`, and builds a new Ethernet frame for the next hop.

---

### Problem 3: Switch Self-Learning

**Question:** A switch has four ports (1, 2, 3, 4). Hosts A, B, C, and D are connected to ports 1, 2, 3, and 4 respectively. The switch's forwarding table starts empty.

The following frames arrive in order:

1. Frame from A (MAC `AA`) to B (MAC `BB`) arrives on port 1.
2. Frame from B (MAC `BB`) to A (MAC `AA`) arrives on port 2.
3. Frame from C (MAC `CC`) to D (MAC `DD`) arrives on port 3.
4. Frame from A (MAC `AA`) to C (MAC `CC`) arrives on port 1.
5. Frame from D (MAC `DD`) to A (MAC `AA`) arrives on port 4.

For each frame, state:
- What does the switch learn?
- What does the switch do with the frame (forward to specific port, flood, or filter)?

---

**Solution:**

| Frame | Learn | Action |
|-------|-------|--------|
| A → B (port 1) | `AA` → port 1 | `BB` unknown → **flood** ports 2, 3, 4 |
| B → A (port 2) | `BB` → port 2 | `AA` known (port 1) → **forward to port 1** only |
| C → D (port 3) | `CC` → port 3 | `DD` unknown → **flood** ports 1, 2, 4 |
| A → C (port 1) | (already known) | `CC` known (port 3) → **forward to port 3** only |
| D → A (port 4) | `DD` → port 4 | `AA` known (port 1) → **forward to port 1** only |

After all five frames, the forwarding table is:

| MAC | Port |
|-----|------|
| AA | 1 |
| BB | 2 |
| CC | 3 |
| DD | 4 |

All hosts have been learned, and subsequent frames will be forwarded without flooding.

---

### Problem 4: Multi-Switch Forwarding

**Question:** Consider the topology below:

A ---(port 1)--- S1 ---(port 3)--- S2 ---(port 2)--- C
                 |                           |
              (port 2)                   (port 3)
                 |                           |
                 B                           D


All forwarding tables start empty. Host A sends a frame to Host D.

(a) What does S1 learn and what does it do with the frame?  
(b) What does S2 learn and what does it do with the frame?  
(c) D replies to A. What does S2 learn and what does it do?  
(d) What does S1 learn from the reply and what does it do?  
(e) After this exchange, what entries are in S1's and S2's forwarding tables?

---

**Solution:**

**(a)** Frame from A to D arrives at S1 on **port 1**.

- **Learn:** `A` → port 1
- **Action:** Destination `D` is unknown → **flood** ports 2 (to B) and 3 (to S2).

B receives the frame but discards it (not for B). S2 receives it on port 1.

**(b)** Frame from A to D arrives at S2 on **port 1** (the trunk link from S1).

- **Learn:** `A` → port 1
- **Action:** Destination `D` is unknown → **flood** ports 2 (to C) and 3 (to D).

C discards; D accepts.

**(c)** D replies to A. Frame arrives at S2 on **port 3**.

- **Learn:** `D` → port 3
- **Action:** Destination `A` is **known** (port 1) → **forward to port 1 only** (toward S1).

**(d)** The reply frame from D to A arrives at S1 on **port 3** (from S2).

- **Learn:** `D` → port 3
- **Action:** Destination `A` is **known** (port 1) → **forward to port 1 only**.

A receives the reply.

**(e)** After the exchange:

**S1's table:**

| MAC | Port |
|-----|------|
| A | 1 |
| D | 3 |

**S2's table:**

| MAC | Port |
|-----|------|
| A | 1 |
| D | 3 |

All subsequent A ↔ D traffic is forwarded directly without flooding. Neither switch ever learns B or C because those hosts never transmitted a frame.

---

### Problem 5: Ethernet Minimum Frame Size Calculation

**Question:** A network uses CSMA/CD on a cable with maximum length 2000 meters. The signal propagation speed is $2 \times 10^8$ m/s. The data rate is 100 Mb/s.

(a) What is the one-way propagation delay $\tau$?  
(b) What is the minimum frame transmission time required for CSMA/CD to work?  
(c) What is the minimum frame size in bits? In bytes?  
(d) If the standard Ethernet minimum frame size is 64 bytes, is this network's required minimum larger, smaller, or the same? Explain.

---

**Solution:**

**(a)** One-way propagation delay:

$$
\tau = \frac{\text{distance}}{\text{propagation speed}} = \frac{2000}{2 \times 10^8} = 10 \times 10^{-6} = 10\;\mu\text{s}
$$

**(b)** CSMA/CD requires the transmission time $T \geq 2\tau$ (round-trip delay):

$$
T_{\text{min}} = 2\tau = 2 \times 10\;\mu\text{s} = 20\;\mu\text{s}
$$

**(c)** Minimum frame size:

$$
L_{\text{min}} = T_{\text{min}} \times R = 20 \times 10^{-6} \times 100 \times 10^6 = 2000\;\text{bits}
$$

In bytes: $2000 / 8 = 250\;\text{bytes}$.

**(d)** The required minimum for this network (250 bytes) is **larger** than the standard Ethernet minimum (64 bytes). This is because:

- The standard 64-byte minimum was designed for 10 Mb/s and 2500 meters ($\tau \approx 25\;\mu\text{s}$).
- At 100 Mb/s (10× faster), bits are 10× shorter in time, so you need 10× more bits to fill the same round-trip window.
- Our cable is slightly shorter (2000 m vs. 2500 m), but the speed increase dominates: $L_{\text{min}} \propto R$.

In practice, Fast Ethernet (100 Mb/s) kept the 64-byte minimum but reduced the maximum network diameter to about 200–400 meters depending on the medium (e.g., 100BASE-TX uses a star topology with switches, eliminating shared collisions entirely).

---

## Generative AI Usage

I used ChatGPT (GPT-4) to help with this problem set:

- It helped formulate realistic problem scenarios based on the lecture material.
- It reviewed my solutions for numerical accuracy.
- It suggested structuring the problems to build from simple frame analysis to multi-switch forwarding.
