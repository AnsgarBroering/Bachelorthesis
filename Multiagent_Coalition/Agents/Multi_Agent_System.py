from tkinter import font
import matplotlib.pyplot as plt
import numpy as np
import random
import math

class Multi_Agent_System:

    def generate_clusters(self, num_coordinates, num_clusters, min_distance):
        coordinates = []

        # Generate random cluster centers
        cluster_centers = []
        for _ in range(num_clusters):
            x = random.uniform(0, 10)
            y = random.uniform(0, 10)
            cluster_centers.append((x, y))

        clusters = {}
        for i in range(cluster_centers):
            clusters[i] = []

        # Generate coordinates near the cluster centers
        while len(coordinates) < num_coordinates:
            for _ in range(num_coordinates):
                cluster_center = random.choice(clusters)
                x = random.gauss(cluster_center[0], 0.5)
                y = random.gauss(cluster_center[1], 0.5)
                new_coord = (x, y)

                # Check the minimum distance to other coordinates
                if all(self.euclidean_distance(new_coord, existing_coord) >= min_distance for existing_coord in coordinates):
                    coordinates.append(new_coord)
                    clusters[cluster_center].append(coordinates[-1])

        return clusters

    def Multi_Agent_System(self):

        xmin, xmax, ymin, ymax = 0, 9, 0, 9
        fig, ax = plt.subplots(figsize=(20, 20))

        ax.set(xlim=(xmin - 1, xmax + 1), ylim=(ymin - 1, ymax + 1), aspect='equal')

        ax.spines['bottom'].set(position="zero", linewidth=2.5)
        ax.spines['left'].set(position="zero", linewidth=2.5)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        ax.text(10.15, 0, "x", fontdict=font, va="center")
        ax.text(0, 10.15, "y", fontdict=font, ha="center")

        x_ticks = np.arange(xmin, xmax)
        y_ticks = np.arange(ymin, ymax)

        ax.set_xticks(x_ticks[x_ticks != x_ticks])
        ax.set_yticks(y_ticks[y_ticks != y_ticks])

        ax.set_xticks(np.arange(xmin, xmax + 1), minor=True)
        ax.set_yticks(np.arange(ymin, ymax + 1), minor=True)
        ax.grid(which='both', color='grey', linewidth=1, linestyle='-', alpha=0.25)

        plt.show()

    def euclidean_distance(self, coord1, coord2):
        x1, y1 = coord1
        x2, y2 = coord2
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def show_graphics(self, result):
        colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']
        for cluster_id, cluster_coords in result.items():
            x_coords = [coord[0] for coord in cluster_coords]
            y_coords = [coord[1] for coord in cluster_coords]
            plt.scatter(x_coords, y_coords, c=colors[cluster_id], label=f'Cluster {cluster_id}')

        plt.xlabel('X-Koordinate')
        plt.ylabel('Y-Koordinate')
        plt.title('Generierte Cluster-Koordinaten')
        plt.legend()
        plt.show()