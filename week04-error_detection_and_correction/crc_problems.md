# Week 4 - Problems with Solution
## Error Detection and Correction: CRC and Code Analysis

---

## Problem 1 — Codeword Properties

Given the code: C = {00000, 11100, 11011, 00111}


### (a) What is the rate of the code?

There are 4 codewords, so:

$$
2^k = 4 \Rightarrow k = 2
$$

Each codeword has length $n = 5$, so:

$$
R = \frac{k}{n} = \frac{2}{5} = 0.4
$$

---

### (b) What is the minimum Hamming distance $d_{min}$?

Compute pairwise distances:

| Pair | Distance |
|------|--------|
| 00000 vs 11100 | 3 |
| 00000 vs 11011 | 4 |
| 00000 vs 00111 | 3 |
| 11100 vs 11011 | 3 |
| 11100 vs 00111 | 4 |
| 11011 vs 00111 | 3 |

$$
d_{min} = 3
$$

---

### (c) How many errors can be detected?

Detection condition:

$$
d_{min} \ge d + 1
$$

So:

$$
d = d_{min} - 1 = 2
$$

**Answer:** Can detect up to **2-bit errors**

---

### (d) How many errors can be corrected?

Correction condition:

$$
d_{min} \ge 2t + 1
$$

$$
t = \left\lfloor \frac{d_{min} - 1}{2} \right\rfloor = 1
$$

**Answer:** Can correct 1-bit error

---

### (e) Received word: 01010

Compute distances:

- To 00000 → 2  
- To 11011 → 2  
- To 11100 → 3  
- To 00111 → 3  

Since there is a tie between two closest codewords, decoding is ambiguous.

**Answer:**
- Cannot reliably correct  
- Should request retransmission (if possible)

---

## Problem 2 — Single-Bit Error Correction Condition

For a message of $k = 1000$ bits, find the minimum number of check bits.

Condition:

$$
n + 1 \le 2^{n-k}
$$

Try values:

- $n = 1009$:  
  $1010 \le 2^9 = 512$ → Wrong

- $n = 1010$:  
  $1011 \le 2^{10} = 1024$ → Correct

So:

$$
n - k = 10
$$

**Answer:** Minimum **10 check bits**

---

## Problem 3 — CRC Encoding

Given:
- Message: $M = 1101$
- Generator: $G = 1011$

### Step 1: Append zeros

Generator has degree $r = 3$

$$
M' = 1101\;000
$$

---

### Step 2: Modulo-2 division

Divide: 1101000 ÷ 1011

Result: Remainder = 001

---

### Step 3: Transmitted frame

$$
T = 1101000 + 001 = 1101001
$$

---

### Verification

Divide $1101001$ by $1011$:

Remainder = 000 → valid codeword

---

## Problem 4 — Conceptual Comparison

Compare three methods:

| Method | Utilization | Reliability |
|------|-----------|------------|
| Error Detection (parity) | High (~0.998) | Good |
| Error Correction | Slightly lower (~0.990) | Good |
| Repetition (1/3) | Very low (~0.333) | Excellent |

---

### Key Observations

- Error detection is more efficient than correction in networking  
- Repetition coding is extremely inefficient  
- Networking protocols prefer:
  - **Detect errors**
  - **Retransmit (e.g., TCP)**

---

## Reflection

A key takeaway is that **error detection is usually preferred over correction** in real networks.

Reason:
- Bandwidth is more valuable than avoiding retransmissions  
- Retransmission is cheap in packet-switched networks  
- CRC provides extremely strong detection with low overhead  

This explains why:
- Ethernet and WiFi use **CRC-32**
- TCP handles retransmission instead of link-layer correction  

---

## Generative AI Usage

I used ChatGPT to assist in generating and refining these problems and solutions.

Specifically:
- Helped construct structured problem statements based on lecture topics (CRC, Hamming distance, error correction)
- Verified step-by-step solutions for correctness (e.g., CRC division, minimum distance calculations)
- Provided alternative explanations to ensure conceptual clarity