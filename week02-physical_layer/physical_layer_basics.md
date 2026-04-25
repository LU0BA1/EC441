# Week 2 - Report
## Understanding the Physical Layer

**Course:** EC 441 - Introduction to Computer Networking
**Week:** 2 - Physical Layer Basics

---

## 1. Introduction

The physical layer is the lowest layer in the network stack. It deals with transmitting raw bits over a communication channel. This week I studied three main topics: transmission media, signal attenuation, and basic digital signaling.

---

## 2. Guided Transmission Media

### 2.1 Twisted Pair Cable

Two insulated copper wires twisted together. Twisting reduces electromagnetic interference.

**Key Parameters:**
- Characteristic impedance: 100Ω (must match transmitter/receiver)
- Attenuation: ~2.5 dB per 100m at 100 MHz
- Propagation speed: ~0.64c
- Categories: Cat 5e (100 MHz), Cat 6 (250 MHz), Cat 8 (2000 MHz)

**Example Calculation:**

| Parameter | Value |
|-----------|-------|
| Transmit power | 30 dBm (1W) |
| Cable loss (100m) | 2.5 dB |
| Received power | 27.5 dBm (0.56W) |
| Power loss | 44% |

### 2.2 Coaxial Cable

Structure: Center conductor, dielectric insulator, outer shield, protective jacket.

**Advantages:**
- Better shielding than twisted pair
- Lower attenuation: 0.5-2 dB per 100m
- Higher bandwidth: DC to 1+ GHz

**Types:**
- RG-6: 75Ω for cable TV, cable modem
- RG-58: 50Ω for legacy Ethernet

### 2.3 Optical Fiber

Light propagates through glass core via total internal reflection.

**Attenuation Comparison:**

| Medium | Attenuation |
|--------|-------------|
| Copper at 100 MHz | ~25 dB/km |
| Fiber at 1550 nm | ~0.2 dB/km |
| Fiber at 1310 nm | ~0.4 dB/km |
| Fiber at 850 nm | ~2.5 dB/km |

**Key Insight:** Fiber has 100× less attenuation than copper!

**Types:**

| Type | Core Diameter | Distance | Use Case |
|------|---------------|----------|----------|
| Single-mode | ~9μm | 100+ km | Long-haul, backbone |
| Multi-mode | 50-62.5μm | ~2 km | Data centers, campus |

**Example from Lecture:**

100 km fiber link at 1550 nm:
- Transmit power: 0 dBm (1 mW)
- Total loss: 20 dB
- Received power: -20 dBm (10 μW)
- Power ratio: 100:1 loss (still usable!)

---

## 3. Understanding Decibels (dB)

### 3.1 Why Use dB?

Multiplication becomes addition, making calculations easier.

**Formula:** dB = 10 log₁₀(P_out / P_in)


**Absolute Power Levels:**
- dBm: relative to 1 mW (0 dBm = 1 mW)
- dBW: relative to 1 W (0 dBW = 1 W)

### 3.2 Key Values to Memorize

| Power Ratio | dB Value |
|-------------|----------|
| 2× | +3 dB |
| 10× | +10 dB |
| 100× | +20 dB |
| 1/2 | -3 dB |
| 1/10 | -10 dB |
| 1/100 | -20 dB |

---

## 4. Link Budget Analysis

Link budget calculates whether received signal strength is sufficient.

**Formula:** P_rx(dBm) = P_tx(dBm) - L_cable(dB) + G_tx(dBi) + G_rx(dBi)


### Example 1: Ethernet Link

From lecture notes:

| Parameter | Value |
|-----------|-------|
| Transmit power | 30 dBm |
| Cable loss (100m) | 2.5 dB |
| Receiver sensitivity | -30 dBm |

**Calculations:**
Received power = 30 - 2.5 = 27.5 dBm
Link margin = 27.5 - (-30) = 57.5 dB
Max length (by attenuation) = (57.5/2.5) × 100m = 2.3 km


*Note: Ethernet standard limits to 100m due to timing, not attenuation.*

### Example 2: Fiber Optic Link

From lecture notes:

| Parameter | Value |
|-----------|-------|
| Transmit power | 10 dBm |
| Fiber loss (0.2 dB/km × 100 km) | 20 dB |
| Splice loss (0.1 dB × 10) | 1 dB |
| Connector loss (0.5 dB × 2) | 1 dB |
| Total loss | 22 dB |
| Receiver sensitivity | -25 dBm |

**Calculations:**
Received power = 10 - 22 = -12 dBm
Link margin = -12 - (-25) = 13 dB



---

## 5. Shannon-Hartley Theorem

**Formula:** C = B log₂(1 + S/N) bits/s



Where:
- C = channel capacity (maximum data rate)
- B = bandwidth (Hz)
- S/N = signal-to-noise ratio (linear, not dB)

### Key Insights:

1. Capacity increases linearly with bandwidth
2. Capacity increases logarithmically with SNR
3. Bandwidth is precious!
4. Can trade SNR for bandwidth

### Examples from Lecture:

**Telephone Channel:**

| Parameter | Value |
|-----------|-------|
| Bandwidth | 3 kHz |
| SNR | 30 dB (1000:1) |
| Capacity | 3000 × log₂(1001) ≈ 30 kbps |

**Ethernet Link:**

| Parameter | Value |
|-----------|-------|
| Bandwidth | 100 MHz |
| SNR | 20 dB (100:1) |
| Capacity | 10⁸ × log₂(101) ≈ 666 Mbps |

*Note: Practical systems achieve 50-90% of Shannon capacity.*

---

## 6. Digital Signaling Fundamentals

### 6.1 Representing Bits

**General form:** x(t) = Σ a_k g(t - kT)



Where:
- a_k = symbol values (from bits)
- g(t) = pulse shape
- T = symbol period

### 6.2 Bit-to-Symbol Mapping

**Unipolar (On-Off Keying):**

| Bit | Value |
|-----|-------|
| 0 | a_k = 0 |
| 1 | a_k = A |

*Simple but wastes energy, has DC component.*

**Bipolar NRZ (Most Common):**

| Bit | Value |
|-----|-------|
| 0 | a_k = -A |
| 1 | a_k = +A |

*Balanced (no DC component), better noise immunity.*

---

## 7. Probability of Error

### 7.1 For Bipolar NRZ

**Bit Error Rate (BER):** P_b = Q(√(2E_b/N₀))



### 7.2 The Q-Function

Q(x) decreases rapidly with x:

| x | Q(x) | Error Rate |
|---|------|------------|
| 3 | 1.3 × 10⁻³ | 1 in 1000 |
| 4 | 3 × 10⁻⁵ | 1 in 30,000 |
| 5 | 3 × 10⁻⁷ | 1 in 3 million |
| 6 | 10⁻⁹ | 1 in 1 billion |

**Key Insight:** Small increase in SNR gives huge decrease in BER. This is called the waterfall effect.

### 7.3 From Lecture Notes

| E_b/N₀ (dB) | Argument | BER |
|-------------|----------|-----|
| 6 dB | Q(2) | 2.3 × 10⁻² |
| 8 dB | Q(2.52) | 6 × 10⁻³ |
| 10 dB | Q(3.16) | 8 × 10⁻⁴ |
| 12 dB | Q(4) | 3 × 10⁻⁵ |
| 15 dB | Q(5.6) | 10⁻⁸ |

---

## 8. Practice Problems

### Problem 1: Simple Link Budget

An office needs to run Ethernet cable 80 meters.

**Given:**
- Transmit power: 20 dBm
- Cable loss: 2.5 dB per 100m
- Receiver sensitivity: -10 dBm

**Solution:**
Loss for 80m = 2.5 × (80/100) = 2 dB
Received power = 20 - 2 = 18 dBm
Margin = 18 - (-10) = 28 dB



**Result:** Signal is sufficient with 28 dB margin.

### Problem 2: Maximum Distance

How far can signal go before reaching sensitivity?

**Given:**
- Transmit power: 15 dBm
- Receiver sensitivity: -25 dBm
- Cable loss: 2.5 dB per 100m

**Solution:**
Total allowable loss = 15 - (-25) = 40 dB
Maximum distance = (40/2.5) × 100 = 1600 m


**Result:** Signal could theoretically go 1600m, but Ethernet standards limit to 100m.

### Problem 3: Fiber vs Copper

Compare loss over 10 km.

**Given:**
- Copper loss: 25 dB/km at 100 MHz
- Fiber loss: 0.2 dB/km at 1550 nm

**Solution:**
Copper total loss = 25 × 10 = 250 dB
Fiber total loss = 0.2 × 10 = 2 dB


**Result:** After 10 km, copper signal is virtually gone, fiber signal is almost as strong as when it started!

---

## 9. Key Takeaways

| Topic | Summary |
|-------|---------|
| **Twisted Pair** | Good for short distances (<100m), ~2.5 dB/100m loss |
| **Coaxial** | Better shielding, lower loss, used for cable TV |
| **Fiber** | 100× less loss than copper, enables long-haul communication |
| **dB** | Makes calculations easier: +3 dB = double, -3 dB = half |
| **Link Budget** | Ensures signal arrives with enough strength |
| **Shannon Capacity** | C = B log₂(1 + SNR), linear in B, log in SNR |
| **Bipolar NRZ** | Preferred signaling: bits map to ±A |
| **BER** | Q(√(2E_b/N₀)), improves dramatically with SNR |

---

## 10. Connection to Networking

Why physical layer matters for networks:

1. **Ethernet limited to 100m** - not by attenuation, but by timing
2. **Fiber enables long-haul links** - 1000s of km possible
3. **Data rates tied to SNR and bandwidth** - better signal = faster speed
4. **Error rates affect protocol design** - wired: BER ~10⁻⁹, wireless: BER 10⁻⁵ to 10⁻³

---

## 11. Questions I Still Have

1. How exactly does twisting wires reduce EMI?
2. What physical mechanism causes thermal noise?
3. How are fiber optic cables joined without significant loss?
4. What is the difference between dB, dBm, and dBi?

---

## 12. AI Usage Statement

I used ChatGPT to help explain complex concepts and check my understanding.

**Process:**
1. **Initial prompts:** "Explain dB with simple examples" and "Walk me through a link budget"
2. **Verification:** Checked all AI explanations against lecture notes
3. **Final work:** Wrote everything in my own words after understanding

The AI helped me grasp difficult concepts, but the learning and final work are my own.

---

## References

- EC 441 Lecture 3 Notes
