from tkinter import font
import matplotlib.pyplot as plt
import numpy as np
import random
import math

class CoordinateSystem:

    coordinates = []
    power_means_clusters = {}             # Saves generated power means for clusters in kW/h
    power_generation_wind_turbines = {}   # Saves the generated power values for each coordinate in kW/h

    def generate_clusters(self,
                          x_range,
                          y_range,
                          number_coordinates,
                          number_clusters,
                          medium_cluster_radius,
                          turbine_distance,
                          seed
                          ):

        if seed != 0:
            random.seed(seed)

        # Generate random cluster centers
        cluster_centers = []
        for _ in range(number_clusters):
            x = round(random.uniform(medium_cluster_radius*2, x_range-medium_cluster_radius*2), 2)
            y = round(random.uniform(medium_cluster_radius*2, y_range-medium_cluster_radius*2), 2)
            new_cluster_coordinate = (x, y)
            if all(self.euclidean_distance(new_cluster_coordinate, existing_coord) >= (medium_cluster_radius*2) for existing_coord in cluster_centers):
                cluster_centers.append(new_cluster_coordinate)
                self.power_means_clusters.update({new_cluster_coordinate: float((random.gauss(0.5, 0.12) ** 2) * 2500)})

        # Counts the number of coordinates for each cluster
        clusters = {}
        for i in cluster_centers:
            clusters[i] = 0

        # ToDo: Solve bug where more coordinates are generated than expected
        # Generate coordinates near the cluster centers
        while len(self.coordinates) < number_coordinates:
            cluster_center = random.choice(cluster_centers)
            x = round(random.gauss(cluster_center[0], medium_cluster_radius), 2)
            y = round(random.gauss(cluster_center[1], medium_cluster_radius), 2)
            new_coord = (x, y)

            # Check the minimum distance to other coordinates
            if all(self.euclidean_distance(new_coord, existing_coord) >= turbine_distance for existing_coord in self.coordinates):
                self.coordinates.append(new_coord)
                self.power_generation_wind_turbines.update({new_coord: self.calculate_power_value(cluster_center)})
                clusters[cluster_center] = clusters[cluster_center]+1

        print(clusters)
        return

    # Calculates the euclidean distance by using the Pythagorean Theory
    def euclidean_distance(self, coord1, coord2):
        x1, y1 = coord1
        x2, y2 = coord2
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def calculate_power_value(self, cluster):
        power_value = self.power_means_clusters.get(cluster) * random.gauss(1, 0.1)
        # If the turbine generates more than 2500 it's turned off because of too much wind force
        if power_value < 0 or power_value > 2500:
            power_value = 0
        return power_value

    # Plots the coordinates
    def plot_coordinates(self, x_limit, y_limit):

        """
        x_coords = [coord[0] for coord in coordinates]
        y_coords = [coord[1] for coord in coordinates]

        plt.scatter(x_coords, y_coords)
        """

        for i, (x, y) in enumerate(self.coordinates):
            plt.scatter(x, y, c='g')
            plt.annotate(f'{round(self.power_generation_wind_turbines.get(self.coordinates[i]), 1)}', (x, y), textcoords="offset points", xytext=(5, 5), ha='center')

        plt.xlabel('X-Koordinate')
        plt.ylabel('Y-Koordinate')
        plt.title('Koordinaten der WKAs mit Leistungen in kW/h')

        if x_limit:
            plt.xlim(0, x_limit)
        if y_limit:
            plt.ylim(0, y_limit)

        plt.show()
