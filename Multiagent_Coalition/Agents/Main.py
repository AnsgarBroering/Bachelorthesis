from Datacollector import Datacollector

if __name__ == "__main__":
    datacollector = Datacollector()
    coordinates = datacollector.start()
    datacollector.show_graphics(coordinates)
