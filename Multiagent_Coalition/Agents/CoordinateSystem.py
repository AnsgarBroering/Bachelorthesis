from tkinter import font
import matplotlib.pyplot as plt
import numpy as np
import random
import math

class CoordinateSystem:

    # Saves all coordinates as tuples in this array
    coordinates = []
    # Saves generated power means for clusters in kW/h
    power_means_clusters = {}
    # Saves the generated power values for each coordinate as a percentile fraction to the rated capacity
    power_generation_wind_turbines = {}
    # The expected average of the power a wind turbine produces (in kW/h)
    POWER_AVERAGE = 900
    # The top limit a wind turbine can produce in power (in kW/h)
    RATED_CAPACITY = 3000

    def generate_clusters(self,
                          x_range,
                          y_range,
                          number_coordinates,
                          number_clusters,
                          medium_cluster_radius,
                          turbine_distance,
                          seed
                          ):
        """
        Generates clusters with all coordinates and the expected power generation for all wind turbines

        :param x_range: The limit of the coordinate system on the x-axis.
        :param y_range: The limit of the coordinate system on the y-axis.
        :param number_coordinates: The number of coordinates this function needs to produce
        :param number_clusters: The number of clusters the function uses to
        :param medium_cluster_radius: The medium radius of a cluster
        :param turbine_distance: The minimal distance between wind turbines
        :param seed: The seed of the random function
        :return: Returns an array of coordinates
        """

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
                self.power_means_clusters.update({new_cluster_coordinate: float((random.gauss(0.5, 0.12) ** 2) * self.RATED_CAPACITY)})

        # Counts the number of coordinates for each cluster
        clusters = {}
        for i in cluster_centers:
            clusters[i] = 0

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
        """
        Calculates the distance between two coordinates.
        :param coord1:
        :param coord2:
        :return: The distance between the coordinates
        """

        x1, y1 = coord1
        x2, y2 = coord2
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def calculate_power_value(self, cluster):
        """
        Calculates the power value in percentage to the RATED_CAPACITY of 3000 MW.
        :param cluster: The function uses the base power value of this cluster.
        :return: Returns a number between 0 and 1.
        """

        power_value = self.power_means_clusters.get(cluster) * random.gauss(1, 0.1)
        # If the turbine generates more than 3000 it's turned off because of too much wind force
        if power_value < 0 or power_value > self.RATED_CAPACITY:
            power_value = 0
        return power_value/3000

    # Plots the coordinates
    def plot_coordinates(self, x_limit, y_limit):

        """
        x_limit = [coord[0] for coord in coordinates]
        y_limit = [coord[1] for coord in coordinates]

        plt.scatter(x_limit, y_limit)
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
