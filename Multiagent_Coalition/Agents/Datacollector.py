import asyncio
class Datacollector:

    # All distances and radii are in kilometers.
    x_distance = float(0)
    y_distance = float(0)
    amount_wind_turbines = int(0)
    amount_clusters = int(0)
    medium_cluster_radius = float(0)
    min_size_cluster = int(0)
    max_size_cluster = int(0)
    min_distance_turbines = float(0)
    min_distance_clusters = float(0)

    def start(self):

        while self.x_distance <= 0:
            try:
                self.x_distance = float(input(f"Length of x in the coordinate system in km: "))
            except:
                print(f"You need to enter a number greater than 0.")

        while self.y_distance <= 0:
            try:
                self.y_distance = float(input(f"Length of y in the coordinate system in km: "))
            except:
                print(f"You need to enter a number greater than 0.")

        while self.amount_wind_turbines < 2:
            try:
                self.amount_wind_turbines = int(input(f"Amount of wind turbines: "))
                if self.amount_wind_turbines < 2:
                    print(f"Amount of wind turbines must be more than 1: ")
            except:
                print(f"You need to enter a number greater than 0.")

        while self.amount_clusters <= 0 | self.amount_clusters > self.amount_wind_turbines:
            try:
                self.amount_clusters = int(input(f"Amount of clusters: "))
                if self.amount_clusters > self.amount_wind_turbines:
                    self.amount_clusters = int(input(f"Amount of clusters must be less or equal than {self.amount_wind_turbines}: "))
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

        while self.max_size_cluster <= 0 | self.max_size_cluster < int(self.amount_wind_turbines / self.amount_clusters) + 1:
            try:
                self.max_size_cluster = int(input(f"Maximal size of clusters: "))
                if self.max_size_cluster < int(self.amount_wind_turbines / self.amount_clusters) + 1:
                    self.max_size_cluster = int(input(f"The cluster size must be greater than {int(self.amount_wind_turbines / self.amount_clusters)}: "))
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