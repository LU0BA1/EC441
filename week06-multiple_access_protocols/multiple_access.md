# Week 6 — Report  
## Sharing the Air: How Multiple Access Protocols Keep Things Orderly

---

## Overview

This report explores the **multiple access problem** — what happens when many devices try to talk on the same channel at the same time — and the three major families of solutions that networking has invented. The focus is on:

1. The inefficiency of fixed division (TDMA, FDMA)
2. The simplicity and low efficiency of ALOHA protocols
3. How carrier sensing (CSMA) and collision detection (CSMA/CD) achieve near‑perfect sharing

These ideas directly shape everyday technologies like WiFi and classic Ethernet.

---

## 1. The Multiple Access Problem

In a **broadcast medium** (e.g., the radio channel WiFi uses, or a coaxial cable in old Ethernet), all devices hear each other’s transmissions. If two send at the same time, their signals overlap — a collision — and both frames are destroyed.

We need a **MAC (Medium Access Control) protocol** — a set of rules that each device follows so that only one talks at a time and lost data is recovered efficiently.

An ideal MAC protocol would give the full link speed to a single user, share it equally among many, need no central controller, and be simple. No real protocol hits all four goals, but the ones studied here get close enough.

---

## 2. Fixed Allocation: TDMA and FDMA — Why They Waste Capacity

**Time Division Multiple Access** (TDMA) cuts time into equal slots, each permanently assigned to one station.

**Frequency Division Multiple Access** (FDMA) does the same but divides the radio frequency range instead.

- **No collisions** — transmissions are separated by time or frequency.
- **Fixed rate** — each station always gets exactly its slice of the total rate.

The problem is **idle stations**: a slot or frequency band assigned to a silent station is wasted, and no one else may use it. Network traffic is bursty — long silences followed by occasional bursts. Under such loads, TDMA and FDMA can waste more than 90% of the channel.

These schemes work well when the load is heavy and uniform (like GSM voice calls), but they fail for LAN‑style data traffic.

---

## 3. Random Access and ALOHA

### 3.1 Pure ALOHA

The simplest possible rule: transmit at once; if a collision happens (detected by the absence of an acknowledgement), wait a random time and try again.

If the transmission time of one frame is $T$, any transmission starting during the window $[t-T,\; t+T]$ will collide with a frame starting at $t$. The collision window is therefore **$2T$**.

Assuming Poisson arrivals with mean offered load $G$ (attempts per frame time), the probability of success is

$$
P_{\text{success}} = e^{-2G}
$$

and the throughput $S$ (successful transmissions per frame time) is

$$
S = G e^{-2G}
$$

The maximum throughput occurs at $G = 1/2$:

$$
S_{\text{max}} = \frac{1}{2e} \approx 0.184
$$

About 18% efficiency — the channel is idle or colliding 82% of the time.

### 3.2 Slotted ALOHA

A small improvement: require all stations to start transmissions only at fixed slot boundaries (slot length $= T$). Now two frames collide only if they begin in the same slot — the collision window shrinks to $T$.

Throughput becomes

$$
S = G e^{-G}, \qquad S_{\text{max}} = \frac{1}{e} \approx 0.368
$$

Exactly **double** pure ALOHA, but still only 37% of the channel is used productively. At peak load, 37% of slots are successful, 37% are empty, and 26% are collisions.

**Key limitation**: ALOHA stations do not listen before transmitting. They gamble, and the odds are never great.

---

## 4. Carrier Sense Multiple Access (CSMA)

On a local cable or radio, the propagation delay $\tau$ between any two devices is tiny compared with frame time $T$ (often $\tau \ll T$). This allows a station to listen before speaking — carrier sensing.

**1‑persistent CSMA**: If the channel is idle → transmit immediately. If busy → wait until it becomes idle, then transmit. Problem: many waiting stations start at once, causing guaranteed collisions.

**Non‑persistent CSMA**: If busy → don’t linger — back off a random time and sense again. This avoids the sure collision but may waste time after the channel clears.

**$p$‑persistent CSMA** (slotted): If idle, transmit with probability $p$ and defer to the next slot with probability $1-p$.

Because collisions now require two stations to sense the channel idle within one propagation delay of each other, CSMA dramatically increases efficiency compared with ALOHA.

---

## 5. CSMA/CD — Collision Detection on the Wire

### 5.1 How It Works

**CSMA with Collision Detection** (CSMA/CD) adds one more rule:

- While transmitting, **keep listening** to the wire.
- If the received signal differs from what you sent → a collision is occurring → **stop immediately** (send a short jam signal, then abort).

Instead of wasting a full frame time $T$ on a collision, a station detects the collision within at most the round‑trip propagation time $2\tau$. Since $\tau \ll T$, CSMA/CD wastes very little channel time on collisions.

### 5.2 The 64‑Byte Minimum Frame

For CSMA/CD to work, a station must **still be transmitting** when the collision echo returns. The transmission time must be at least $2\tau$. This yields the minimum frame size:

$$
L_{\text{min}} = 2\tau R
$$

For classic 10 Mb/s Ethernet on a 2500 m cable ($\tau \approx 25\;\mu\text{s}$):

$$
L_{\text{min}} = 2 \times 25\;\mu\text{s} \times 10\;\text{Mb/s} = 500\;\text{bits} = 64\;\text{bytes}.
$$

The 64‑byte minimum frame size persists in every modern Ethernet standard — a direct consequence of the physics of CSMA/CD.

### 5.3 Binary Exponential Backoff

After a collision, the station backs off for a random time. The backoff range doubles after each successive collision:

- 1st collision: wait 0 or 1 slot time
- 2nd collision: wait 0 … 3 slot times
- 3rd collision: wait 0 … 7 slot times
- …up to a maximum of 1023 slot times.

This **exponential backoff** adapts to the load: short waits when traffic is light, longer waits when traffic is high. The same idea appears later in TCP congestion control.

### 5.4 Efficiency

For large frames (small $a = \tau / T$), CSMA/CD efficiency is approximately

$$
\eta = \frac{1}{1 + 5a}.
$$

As $a \to 0$ (long frames on short cables), $\eta \to 1$. In modern switched Ethernet, every device has a dedicated full‑duplex link to the switch — no collisions occur, and CSMA/CD is never exercised, but the frame format and minimum size remain.

---

## 6. Protocol Comparison

| Protocol | Max Throughput | Collision Window | Sync Required |
|----------|---------------|------------------|----------------|
| Pure ALOHA | 18.4 % | $2T$ | No |
| Slotted ALOHA | 36.8 % | $T$ | Yes (slots) |
| CSMA/CD (small $a$) | → 100 % | $2\tau$ | No (if 1‑persistent) |

**Key insight**: Listening before transmitting (CSMA) and detecting collisions early (CD) together turn a wasteful shared channel into a near‑perfect pipeline.

---

## 7. Reflection

Before studying these protocols, I assumed that the only way to share a channel fairly was with a central controller or assigned time slots. ALOHA seemed almost naive — “just shout and hope for the best” — yet its 18% efficiency was considered acceptable for the 1970s satellite network it was designed for. The step from pure ALOHA to slotted ALOHA doubled throughput by simply aligning transmissions to slot boundaries, and then CSMA/CD pushed efficiency above 90% by leveraging the fact that signal propagation is fast compared with frame length. This progression shows that great engineering is often about exploiting the specific properties of the environment — here, the ratio $\tau/T$ — rather than inventing entirely new mechanisms.

The 64‑byte minimum Ethernet frame is a particularly satisfying example of physical constraints shaping protocol design. It didn’t appear out of nowhere; it is exactly $2\tau R$ for the worst‑case cable length.

---

## 8. Conclusion

Multiple access protocols govern how devices share a common transmission medium. Fixed allocation (TDMA, FDMA) wastes capacity under bursty traffic. ALOHA offers simplicity at the cost of low efficiency. CSMA and CSMA/CD exploit fast propagation to achieve near‑full utilization, forming the foundation of Ethernet and influencing modern wireless protocols. The evolution from ALOHA to switched Ethernet reflects a broader networking theme: understand the physical limits, then design the protocol to work as close to them as possible.

---

## Generative AI Usage

I used ChatGPT and Claude to assist with this report:

- They helped restructure my initial jumble of ideas into a clean, logical flow.
- They checked my throughput equations and ensured the numerical values (18.4%, 36.8%) were correctly derived.
- They suggested clarifying the role of $\tau$ and $a$ in CSMA/CD efficiency.
- I wrote the reflection and conclusion myself to make sure the voice was my own.