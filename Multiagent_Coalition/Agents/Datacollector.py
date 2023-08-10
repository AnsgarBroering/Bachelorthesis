import math

class Datacollector:

    # All distances and radii are in kilometers.
    x_range = float(0)
    y_range = float(0)
    number_wind_turbines = int(0)
    number_clusters = int(0)
    medium_cluster_radius = float(0)
    min_size_cluster = int(0)
    max_size_cluster = int(0)
    min_distance_turbines = float(0)
    min_distance_clusters = float(0)
    seed = int(0)

    def start(self):
        if input("Do you want to use the standard input? (y/n): ") == "y":
            self.x_range = 15
            self.y_range = 15
            self.number_wind_turbines = 15
            self.number_clusters = 5
            self.medium_cluster_radius = 0.7
            self.min_size_cluster = 2
            self.max_size_cluster = 5
            self.min_distance_turbines = 0.2
            self.min_distance_clusters = 2

        else:
            while self.x_range <= 0:
                try:
                    self.x_range = float(input(f"Length of x in the coordinate system in km: "))
                except:
                    print(f"You need to enter a number greater than 0.")

            while self.y_range <= 0:
                try:
                    self.y_range = float(input(f"Length of y in the coordinate system in km: "))
                except:
                    print(f"You need to enter a number greater than 0.")

            while self.number_wind_turbines < 2:
                try:
                    self.number_wind_turbines = int(input(f"Amount of wind turbines: "))
                    if self.number_wind_turbines < 2:
                        print(f"Amount of wind turbines must be more than 1: ")
                except:
                    print(f"You need to enter a number greater than 0.")

            while self.number_clusters <= 0 or self.number_clusters > self.number_wind_turbines:
                try:
                    self.number_clusters = int(input(f"Amount of clusters: "))
                    if self.number_clusters > self.number_wind_turbines:
                        self.number_clusters = int(input(f"Amount of clusters must be less or equal than {self.number_wind_turbines}: "))
                except:
                    print(f"You need to enter a number greater than 0.")

            while self.medium_cluster_radius <= 0:
                try:
                    self.medium_cluster_radius = float(input(f"Medium radius of clusters: "))
                except:
                    print(f"You need to enter a number greater than 0.")

            while self.min_size_cluster <= 0:
                try:
                    self.min_size_cluster = int(input(f"Minimal size of clusters: "))
                    if self.min_size_cluster <= 0:
                        self.min_size_cluster = int(input(f"Amount of clusters must be more than 0: "))
                except:
                    print(f"You need to enter a number greater than 0.")

            while self.max_size_cluster <= 0 or self.max_size_cluster < int(self.number_wind_turbines / self.number_clusters) + 1:
                try:
                    self.max_size_cluster = int(input(f"Maximal size of clusters: "))
                    if self.max_size_cluster < int(math.ceil(self.number_wind_turbines / self.number_clusters)):
                        self.max_size_cluster = int(input(f"The cluster size must be greater than {int(self.number_wind_turbines / self.number_clusters)}: "))
                except:
                    print(f"You need to enter a number greater than 0.")

            while self.min_distance_turbines <= 0:
                try:
                    self.min_distance_turbines = float(input(f"Minimal distance of turbines: "))
                except:
                    print(f"You need to enter a number greater than 0.")

            while self.min_distance_clusters <= 0:
                try:
                    self.min_distance_clusters = float(input(f"Minimal distance of clusters: "))
                except:
                    print(f"You need to enter a number greater than 0.")

        self.seed = input(f"Enter a seed or enter 0 for a random seed: ")
