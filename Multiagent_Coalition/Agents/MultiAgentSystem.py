import asyncio
import random

from mango import Agent, create_container
from mango.util.clock import AsyncioClock, ExternalClock
from WindTurbineAgent import WindTurbineAgent

class MultiAgentSystem:

    _container = 0
    agents = []
    REQUEST_COUNT = 5
    CONTAINER_ADDRESS = ("localhost", 5555)


    async def create_container_with_agents(self, coordinates, power_generation, starting_coalition_value):
        """
        To create the agents which control the wind turbine. The coordinates and their generated power is needed. First
        a container gets created and then all agents. All agents also get the information of their neighbors.
        :param coordinates: The coordinates of the wind turbines as tuples in an array
        :param power_generation: The expected power generation as fraction of the rated capacity of 3000 in a dictionary
        :param starting_coalition_value: The starting value a coalition has before it's in a coalition
        """

        # Create a container with a clock and allocate all new agents to this container
        clock = AsyncioClock()
        self._container = await create_container(addr=self.CONTAINER_ADDRESS, clock=clock)
        for i in coordinates:
            self.agents.append(WindTurbineAgent(self._container,
                                                self.CONTAINER_ADDRESS,
                                                i,
                                                power_generation.get(i),
                                                starting_coalition_value
                                                ))
        # Lets all agents know their neighbor agents
        for i, agent in enumerate(self.agents):
            agent.set_available_agents(self.agents)

        # Start simulation
        if input(f"Do you want to start the simulation with this dataset? (y/n): ") == 'y':
            await self.start_simulation()

        # Shutdown all
        await self.shutdown_agents()
        await self.shutdown_container()

    async def start_simulation(self):
        """
        Commands all agents to start the requesting process.
        """
        shuffled_agents = self.agents
        random.shuffle(shuffled_agents)
        for i, agent in enumerate(shuffled_agents):
            await agent.initiate_requests(self.REQUEST_COUNT, i)
        await asyncio.sleep(30)

    async def plot_coalitions(self):
        """
        Future function to plot all coalitions in a coordinate system
        :return:
        """
        pass

    # This method shutdowns all agents
    async def shutdown_agents(self):
        """
        Shutsdown all agents.
        """

        for i, agent in enumerate(self.agents):
            await agent.shutdown()
        print("Shutdown of all agents complete.")

    # This method shutdowns the container
    async def shutdown_container(self):
        """
        Shutsdown the container.
        """

        await self._container.shutdown()
        print("Shutdown of the container complete.")
