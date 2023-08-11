import numpy as np
from numpy import log
import matplotlib.pyplot as plt

def gaussian(x, mu, sigma):
    return (1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)) * 0.2 + 0.5

def linear(x):
    return np.ln(x)

mu = 0.3
sigma = 0.1

x = np.linspace(0, 1, 1000)
# y = gaussian(x, mu, sigma)
y = linear(x)

plt.xlim(0, 1)
plt.ylim(0, y)

plt.plot(x, y)
plt.xlabel('Erbrachter Leistung in % zum Nennwert')
plt.ylabel('Gewichtung des Leistungsprofils')
plt.title('Gaussische Verteilung der Leistungsprofile')
plt.grid(True)
plt.show()
