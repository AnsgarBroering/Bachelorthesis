import random
import matplotlib.pyplot as plt

def divide_into_groups(coordinates, group_size):
    groups = [coordinates[i:i+group_size] for i in range(0, len(coordinates), group_size)]
    return groups

# Beispielaufruf
coordinates = [(1, 1), (15, 2), (2, 11), (17, 8), (9, 13), (11, 5), (13, 14), (15, 12), (17, 18), (19, 20), (3, 6), (5, 2)]
random.shuffle(coordinates)
group_size = 5

groups = divide_into_groups(coordinates, group_size)

# Plot der Punkte und Verbindungen in unterschiedlichen Farben
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

for i, group in enumerate(groups):
    x_coords = [coord[0] for coord in group]
    y_coords = [coord[1] for coord in group]
    plt.scatter(x_coords, y_coords, c=colors[i])
    plt.plot(x_coords + [x_coords[0]], y_coords + [y_coords[0]], c=colors[i])

plt.xlabel('X-Koordinate')
plt.ylabel('Y-Koordinate')
plt.title('Beispiel einer Koalitionensstruktur')
plt.show()