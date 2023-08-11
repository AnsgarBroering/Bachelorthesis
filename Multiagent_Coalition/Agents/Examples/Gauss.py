import random
import matplotlib.pyplot as plt


def generate_gaussian_numbers(mean, std_dev, num_numbers):
    numbers = [random.gauss(mean, std_dev)**2 for _ in range(num_numbers)]
    return numbers


# Beispielaufruf
mean = 0.58       # Passen Sie den gewuenschten Mittelwert an
std_dev = 0.12   # Passen Sie die gewuenschte Standardabweichung an
num_numbers = 100000

numbers = generate_gaussian_numbers(mean, std_dev, num_numbers)

plt.hist(numbers, bins=50, density=True, alpha=0.7, color='g')
plt.xlabel('Leistungsabweichung')
plt.ylabel('Häufigkeit')
plt.title('Leistungsschwankung allgemein')
plt.show()
