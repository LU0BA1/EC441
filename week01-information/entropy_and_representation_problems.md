#Week 1 – Information: Sources & Representation
Type: Problem with Solutions

##Problem 1 – Self-Information

A network sensor reports whether a packet is successfully delivered or dropped.

A packet is dropped with probability 0.05.

Using the formula:

I(p) = -log₂(p)

I(drop) = -log₂(0.05)

log₂(0.05) ≈ -4.32

So,

I(drop) ≈ 4.32 bits

This means a dropped packet gives about 4.32 bits of information because it is rare.

---

##Problem 2 – Entropy of a Biased System

Suppose:

- P(success) = 0.95

- P(drop) = 0.05

Entropy formula:

H(X) = -[p₁ log₂(p₁) + p₂ log₂(p₂)]

H = -[0.95 log₂(0.95) + 0.05 log₂(0.05)]

log₂(0.95) ≈ -0.074
log₂(0.05) ≈ -4.32

H = -(0.95 × -0.074 + 0.05 × -4.32)

H ≈ 0.286 bits

So on average, each packet gives about 0.29 bits of information.

Because the system is very predictable (mostly success), entropy is small.

---

##Problem 3 – ASCII vs UTF-8

Consider the text:

Hello 世界

ASCII:

- Can only represent basic English characters

- Cannot represent Chinese characters

So ASCII cannot encode this full string.

UTF-8:

- "Hello" = 5 bytes

- Space = 1 byte

- Each Chinese character = 3 bytes

Total:

5 + 1 + 3 + 3 = 12 bytes

UTF-8 works for all languages but may use more bytes for non-English characters.

---

##Problem 4 – Base64 Overhead

Base64 encoding:

3 bytes → 4 ASCII characters

Overhead:

(4 − 3) / 3 = 1/3 = 33%

So Base64 increases size by about 33%.

We use it because some systems only allow text, not raw binary.

---

##Problem 5 – Uncompressed Video Data Rate

1080p video:
1920 × 1080 pixels
3 bytes per pixel (RGB)
30 frames per second

Bytes per frame:

1920 × 1080 × 3 = 6,220,800 bytes ≈ 6.2 MB

Data rate:

6.2 MB × 30 = 186 MB/s

Convert to bits:

186 × 8 ≈ 1488 Mb/s ≈ 1.5 Gb/s

Uncompressed video needs about 1.5 Gb/s.

Typical streaming uses about 5–8 Mb/s.

This shows why compression is necessary.

---

##Problem 6 – SI vs Binary Prefix

1 TB (SI) = 1,000,000,000,000 bytes

1 GiB = 2³⁰ = 1,073,741,824 bytes

1,000,000,000,000 ÷ 1,073,741,824 ≈ 931 GiB

This is why a “1 TB” drive appears as about 931 GiB on a computer.