### Lab Overview

This lab uses Python's standard-library `ipaddress` module to explore IPv4 addressing, CIDR notation, subnetting, and special address ranges. No external dependencies are required — the `ipaddress` module is included in Python 3.3+.

**Course Topic:** Network layer: forwarding, routing, IP addressing, CIDR, subnetting  
**Layer:** Network  
**Type:** Lab

---

### Objectives

1. Perform basic network arithmetic (network address, broadcast address, netmask, usable hosts).
2. Subnet a given address block into equal-sized subnets.
3. Demonstrate the alignment rule for valid subnets.
4. Check whether two hosts are in the same subnet.
5. Identify special-purpose address ranges (RFC 1918, loopback, link-local, multicast).
6. Observe real interface addresses and relate them to the lab computations.

---

### Part 1: Basic Network Arithmetic

**Script:** `part1.py`

**What it does:** Defines a `/24` network and prints its network address, broadcast address, netmask, total addresses, first usable host, and last usable host.

**Output:**
=== Basic Network Arithmetic ===
Network:            192.168.10.0/24
Network address:    192.168.10.0
Broadcast address:  192.168.10.255
Netmask:            255.255.255.0
Prefix length:      /24
Total addresses:    256
Usable hosts:       254
First usable host:  192.168.10.1
Last usable host:   192.168.10.254


**Why this matters:** A `/24` prefix allocates 32 − 24 = 8 bits for hosts, yielding 2^8 = 256 total addresses. Two addresses are reserved: the network address (all host bits 0) and the broadcast address (all host bits 1). The remaining 254 addresses are usable for hosts. Every network engineer must be able to do this calculation in their head.

---

### Part 2: Subnetting an Address Block

**Script:** `part2.py`

**What it does:** Divides `192.168.10.0/24` into 4 equal `/26` subnets. Borrows 2 bits from the host portion (2^2 = 4 subnets), each with 64 total addresses and 62 usable hosts.

**Output:**
Subnet 0: 192.168.10.0/26
  Network address:  192.168.10.0
  Broadcast:        192.168.10.63
  Usable hosts:     192.168.10.1 – 192.168.10.62
  Total usable:     62

Subnet 1: 192.168.10.64/26
  Network address:  192.168.10.64
  Broadcast:        192.168.10.127
  Usable hosts:     192.168.10.65 – 192.168.10.126
  Total usable:     62

Subnet 2: 192.168.10.128/26
  Network address:  192.168.10.128
  Broadcast:        192.168.10.191
  Usable hosts:     192.168.10.129 – 192.168.10.190
  Total usable:     62

Subnet 3: 192.168.10.192/26
  Network address:  192.168.10.192
  Broadcast:        192.168.10.255
  Usable hosts:     192.168.10.193 – 192.168.10.254
  Total usable:     62


**Verification:** 4 × 64 = 256 total addresses. The entire original `/24` is accounted for with no waste and no overlap. In a real network, these four subnets would be isolated broadcast domains — traffic between them must pass through a router.

---

### Part 3: The Alignment Rule

**Script:** `part3.py`

**What it does:** Demonstrates that a valid subnet's network address must be a multiple of the block size. For a `/26` (block size 64), valid network addresses end in `.0`, `.64`, `.128`, `.192`.

**Output:**
Valid /26 networks:
  192.168.1.0/26: network = 192.168.1.0 (block multiple ✓)
  192.168.1.64/26: network = 192.168.1.64 (block multiple ✓)
  192.168.1.128/26: network = 192.168.1.128 (block multiple ✓)
  192.168.1.192/26: network = 192.168.1.192 (block multiple ✓)

Attempting invalid network: 192.168.1.10/26
  strict=False allows it, but network portion is .0, not .10
  Actual network: 192.168.1.0
  Host bits present: 0 ≠ 0 (violates alignment)


**Why alignment matters:** If a network address is not aligned to its block boundary, the bitwise AND with the subnet mask doesn't work cleanly — the CIDR prefix no longer accurately describes the block. The `ipaddress` module enforces this with `strict=True` by default, which catches misconfigurations before they reach a real router.

---

### Part 4: Same-Subnet Check

**Script:** `part4.py`

**What it does:** Determines whether two hosts are in the same `/26` subnet using both manual bitwise operations and the `ipaddress` module's built-in methods.

**Output:**
=== Same-Subnet Checks (Prefix /26) ===

192.168.10.75 and 192.168.10.100: SAME subnet (bitwise: True, pythonic: True)
192.168.10.75 and 192.168.10.130: DIFFERENT subnets (bitwise: False, pythonic: False)
10.0.0.5 and 10.0.0.200: DIFFERENT subnets (bitwise: False, pythonic: False)
172.16.5.1 and 172.16.6.1: DIFFERENT subnets (bitwise: False, pythonic: False)


**Why this matters:** Two hosts on different subnets cannot communicate directly at Layer 2 — their traffic must pass through a router, even if they are physically connected to the same switch. Subnet boundaries are logical, not physical. This check is exactly what a host performs when deciding whether to ARP for the destination directly or ARP for the default gateway instead.

---

### Part 5: Special-Purpose Address Ranges

**Script:** `part5.py`

**What it does:** Tests eight addresses across different special-purpose ranges (RFC 1918 private, loopback, link-local, multicast, public, carrier-grade NAT) and prints their classification.

**Output:**
=== Special-Purpose IPv4 Address Identification ===

10.0.0.1         — RFC 1918 private (10.0.0.0/8)
    is_private:     True
    is_loopback:    False
    is_link_local:  False
    is_multicast:   False
    is_global:      False

172.16.5.1       — RFC 1918 private (172.16.0.0/12)
    is_private:     True
    is_loopback:    False
    is_link_local:  False
    is_multicast:   False
    is_global:      False

192.168.1.42     — RFC 1918 private (192.168.0.0/16)
    is_private:     True
    is_loopback:    False
    is_link_local:  False
    is_multicast:   False
    is_global:      False

127.0.0.1        — Loopback
    is_private:     True
    is_loopback:    True
    is_link_local:  False
    is_multicast:   False
    is_global:      False

169.254.23.45    — Link-local (APIPA)
    is_private:     True
    is_loopback:    False
    is_link_local:  True
    is_multicast:   False
    is_global:      False

224.0.0.5        — Multicast (OSPF all routers)
    is_private:     False
    is_loopback:    False
    is_link_local:  False
    is_multicast:   True
    is_global:      True

8.8.8.8          — Public (Google DNS)
    is_private:     False
    is_loopback:    False
    is_link_local:  False
    is_multicast:   False
    is_global:      True

100.64.0.1       — Carrier-Grade NAT (RFC 6598)
    is_private:     False
    is_loopback:    False
    is_link_local:  False
    is_multicast:   False
    is_global:      False


**Observations:**

- `is_private` returns `True` for RFC 1918, loopback, and link-local — essentially any address not routable on the public internet.
- `is_global` is the most reliable single test for "will this address work on the public internet."
- Carrier-Grade NAT addresses (`100.64.0.0/10`) are `is_global = False` but `is_private = False` — they occupy a middle ground as "shared address space" used by ISPs internally.
- If you ever see `169.254.x.x` on an interface, DHCP has failed and the host self-assigned a link-local address.

---

## Key Takeaways

- **Network arithmetic is deterministic**: Given a prefix, the network address, broadcast address, and usable host range are all computable with simple bitwise operations.

- **Subnetting extends the prefix** to create smaller, isolated broadcast domains. Each borrowed bit doubles the number of subnets and halves the number of hosts per subnet.

- **Alignment ensures subnet boundaries** are cleanly representable as CIDR prefixes. A `/26` must begin at a multiple of 64.

- **Same-subnet determination** is a bitwise AND with the subnet mask — it's the exact operation a host performs to decide whether to ARP directly or use the default gateway.

- **Special addresses** (RFC 1918, loopback, link-local) are not globally routable. The `ipaddress` module identifies them reliably.

- **Real interfaces confirm the theory**: the `brd` field in `ip addr show` matches the broadcast address the kernel computed from the prefix.

---

## Generative AI Usage

I used ChatGPT to assist with this lab:

- It suggested using the `ipaddress` standard-library module as the foundation.
- It reviewed the code for correctness (subnet iteration, bitmask operations, strict vs. non-strict network creation).
- It helped format the output and align the explanations with Lectures 13 and 14.


