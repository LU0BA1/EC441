# Week 3 - Report  
## Wireless Communication Tradeoffs: Path Loss, Modulation, and Capacity

---

## Overview

Wireless communication fundamentally differs from wired systems due to path loss, interference, and shared spectrum constraints. This report analyzes three core mechanisms:

1. Path loss and propagation  
2. Modulation (QAM)  
3. Cellular frequency reuse  

These collectively determine range, data rate, and reliability in real networks.

---

## 1. Path Loss and Its Impact

### Free Space Path Loss (FSPL)

$$
L_{FSPL} = 32.45 + 20\log_{10}(f_{MHz}) + 20\log_{10}(d_{km})
$$

Key properties:
- 10× distance → +20 dB loss  
- 10× frequency → +20 dB loss  

Implication: Higher frequency systems (e.g., 5 GHz WiFi) have shorter range.

---

### Real-World Path Loss

$$
L(d) = L_0 + 10n \log_{10}(d/d_0)
$$

Typical values:
- $n = 2$: free space  
- $n = 3–5$: indoor/urban  

Implication:
- Obstacles significantly increase signal attenuation  
- Indoor environments can reach 30–50 dB loss per decade

---

### Fading Effects

- **Shadow fading:** slow variation (obstacles)  
- **Multipath fading:** fast variation (signal interference)  

Multipath can cause 20–30 dB fluctuations.

---

### Key Insight

Wireless links are inherently unstable. Systems must include:
- Fading margins (10–30 dB)
- Robust design for variability

---

## 2. Modulation and Tradeoffs

### Why Modulation?

Baseband transmission is impractical because:
- Antennas would be too large  
- Signals cannot be separated  
- Propagation is inefficient  

Modulation enables:
- Spectrum sharing  
- Practical antenna sizes  
- Multiple users  

---

### Quadrature Amplitude Modulation (QAM)

$$
s(t) = I(t)\cos(2\pi f_ct) - Q(t)\sin(2\pi f_ct)
$$

- Uses both amplitude and phase  
- Encodes data in I/Q components  

---

### Modulation Tradeoffs

| Modulation | Bits/Symbol | Reliability |
|------------|------------|------------|
| BPSK       | 1          | Very high |
| QPSK       | 2          | High |
| 16-QAM     | 4          | Medium |
| 64-QAM     | 6          | Low |
| 256-QAM    | 8          | Very low |

Higher order modulation:
- Increases data rate  
- Requires higher SNR  
- More sensitive to noise  

---

### Adaptive Modulation

Modern systems dynamically adjust:
- Poor channel → low-order (robust)  
- Good channel → high-order (fast)  

---

### Key Insight

$$
\text{Higher Data Rate} \leftrightarrow \text{Lower Reliability}
$$

---

## 3. Cellular Frequency Reuse

### Problem

Spectrum is limited and cannot be uniquely assigned to all users.

---

### Solution: Frequency Reuse

Divide area into cells:
- Reuse frequencies in distant cells  
- Increase overall capacity  

Cluster size $N$:
- Small $N$: high capacity, high interference  
- Large $N$: low interference, low capacity  

---

### Reuse Distance

$$
D = R\sqrt{3N}
$$

Larger $N$ → better signal quality, less efficiency.

---

### Modern Systems

Older systems:
- $N = 3, 4, 7$

Modern LTE/5G:
- **Reuse factor = 1**

Enabled by:
- Beamforming  
- Interference coordination  
- Advanced receivers  

---

### Sectoring

Cells divided into sectors (typically 3):
- ~3× capacity increase  
- Reduced interference  

---

### Key Insight

Capacity scaling relies on:
- Spatial reuse  
- Directionality  
- Interference management  

---

## 4. System-Level Tradeoffs

| Factor | Improves | Worsens |
|------|--------|--------|
| Higher frequency | Capacity | Range |
| Higher QAM | Throughput | Reliability |
| Smaller cells | Capacity | Cost |
| Higher power | Coverage | Interference |

---

## 5. Reflection

Wireless systems are constrained by physics:

- Signal strength decays rapidly  
- Interference is unavoidable  
- Performance is probabilistic  

Unlike wired systems:
- Increasing power has diminishing returns  
- Capacity depends on spatial reuse  

Modern networks rely on:
- Adaptation  
- Statistical margins  
- Coordination across cells  

---

## 6. Conclusion

Wireless communication balances:

- Signal degradation (path loss, fading)  
- Efficiency (modulation)  
- Capacity (frequency reuse)  

These constraints directly impact:
- WiFi performance  
- Cellular coverage  
- Overall network reliability  

---

## Generative AI Usage

I used ChatGPT to help structure this report and verify technical explanations of path loss, modulation, and frequency reuse.

Specifically:
- Generated an initial outline covering key physical-layer tradeoffs
- Clarified relationships between SNR, modulation order, and reliability
- Checked consistency of formulas (e.g., FSPL and path loss models)
