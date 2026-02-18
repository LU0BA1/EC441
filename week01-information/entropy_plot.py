import numpy as np
import matplotlib.pyplot as plt

p = np.linspace(0.001, 0.999, 1000)
H = -p*np.log2(p) - (1-p)*np.log2(1-p)

plt.plot(p, H)
plt.xlabel("p")
plt.ylabel("Entropy H(p)")
plt.title("Entropy of a Bernoulli Random Variable")
plt.show()
