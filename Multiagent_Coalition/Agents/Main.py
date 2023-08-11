import asyncio
from Datacollector import Datacollector
from CoordinateSystem import CoordinateSystem
from MultiAgentSystem import MultiAgentSystem

if __name__ == "__main__":

    datacollector = Datacollector()
    coordinate_system = CoordinateSystem()

    datacollector.start()
    # ToDo: Implement collected data into the following method call
    coordinate_system.generate_clusters(
        x_range=datacollector.x_range,
        y_range=datacollector.y_range,
        number_coordinates=datacollector.number_wind_turbines,
        number_clusters=datacollector.number_clusters,
        medium_cluster_radius=datacollector.medium_cluster_radius,
        turbine_distance=datacollector.min_distance_turbines,
        seed=datacollector.seed
    )

    # coordinate_system.plot_coordinates(datacollector.x_range, datacollector.y_range)

    if input(f"Do you want to create the multi agent system? (y/n): ") == "y":
        agent_system = MultiAgentSystem()
        asyncio.run(agent_system.create_container_with_agents(coordinate_system.coordinates,
                                                              coordinate_system.power_generation_wind_turbines,
                                                              datacollector.starting_coalition_value
                                                              ))
        # ToDo: Start simulation
