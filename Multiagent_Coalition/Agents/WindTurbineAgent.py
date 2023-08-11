import asyncio
import numpy as np
from mango import Agent
from mango.messages.message import Performatives
from mango.util.scheduling import InstantScheduledProcessTask
from mango.util.clock import AsyncioClock, ExternalClock
import math
import random
from CodecMessages import RequestMessage, AdmissionMessage, RefusalMessage

class WindTurbineAgent(Agent):
    """
    This class is an instance of the Agent class. This is the only Agent class in this program. All agents have the
    same role.
    """

    _container = 0                  # the container of the agent
    _container_address = []         # the container address of this container
    location_coordinate = [0, 0]    # the position of the agent (wind turbine) as coordinate
    expected_power_generation = 0   # the expected power generation for the next time period
    _current_coalition_value = 0    # the current coalition value ready to
    _current_coalition_agents = []  # current agents in coalition with this agent
    _neighbor_agents = []           # classes of all neighboring agents
    _available_agents = {}          # agent id and their availability
    _depleted_request_pool = False  # is all available agents are used up this goes "True"
    _is_done = False                # is "True" when in at least one coalition
    request_count = 0               # this is the maximal amount of requests before the agent stops requesting
    POWER_AMPLITUDE = 0.2           # the height of the biggest spike of the power value function
    POWER_FUNCTION_HEIGHT = 0.5     # here the function hits the y-axis of the power value function
    POWER_FUNCTION_MU = 0.3         # the biggest spike of the power value function is at this x-axis
    POWER_FUNCTION_SIGMA = 0.1      # the standard deviation of the power value function

    def __init__(self, container, address, coordinate, power, starting_coalition_value):
        super().__init__(container)
        self._container = container
        self._container_address = address
        self.location_coordinate = coordinate
        self.expected_power_generation = power
        self._current_coalition_value = starting_coalition_value
        self._current_coalition_agents.append(self.aid)
        print(f"My id is {self.aid}.")

    async def initiate_requests(self, request_count, delay_in_seconds):
        self.request_count = request_count
        self.schedule_timestamp_task(coroutine=self.start_requests(),
                                     timestamp=self.current_timestamp + delay_in_seconds)
        return

    async def start_requests(self):
        """
        With this method the requests are started by MultiAgentSystem.
        """

        # Checks if any agents are still available
        available_agents = [key for key, value in self._available_agents.items() if value]
        # If any agent is available a message is sent to it
        if available_agents:
            request_receiver = random.choice(available_agents)
            print(f"{self.aid} started sending a message to {request_receiver} at {self._container_address}.")
            message_content = RequestMessage(self.aid, self.location_coordinate, self.expected_power_generation)

            acl_meta = {"sender_addr": self._context.addr, "sender_id": self.aid,
                        "performative": Performatives.inform}
            self.schedule_instant_task(
                self._context.send_acl_message(
                    content=message_content,
                    receiver_addr=self._container_address,
                    receiver_id=request_receiver,
                    acl_metadata=acl_meta,
                )

            )
            # await self.send_message(message_content, self._container_address, request_receiver)

        else:
            self._depleted_request_pool = True
        return

    async def handle_message(self, content, meta):
        """
        When a message is received it gets handled here. The content can be of the following types:
        RequestMessage, AdmissionMessage, RefusalMessage
        """

        print(f"{self.aid} has received a message from {meta}.")
        if isinstance(content, RequestMessage):
            if not self._available_agents.get(content.agent_id):
                message_content = RefusalMessage(content.agent_id, self._current_coalition_agents)
                await self.send_message(message_content, self._container_address, content.agent_id)
                return

            calculated_coalition_value = self.calculate_coalition_value(content.coordinate, content.power_profile)
            if self._current_coalition_value == 0 or self._current_coalition_value < calculated_coalition_value:
                self._current_coalition_agents.append(content.agent_id)
                self._current_coalition_value = calculated_coalition_value
                self._is_done = True
                print(f"{self.aid} is done searching.")

                message_content = AdmissionMessage(content.agent_id, self._current_coalition_value)
                for i, agent in enumerate(self._current_coalition_agents):
                    if agent.aid != self.aid:
                        await self.send_message(message_content, self._container_address, agent.aid)
            else:
                self._available_agents.update({content.agent_id: False})
                message_content = RefusalMessage(content.agent_id, self._current_coalition_agents)
                for i, agent in enumerate(self._current_coalition_agents):
                    if agent.aid != self.aid:
                        await self.send_message(message_content, self._container_address, agent.aid)

        elif isinstance(content, AdmissionMessage):
            self._current_coalition_agents.append(content.agent_id)
            self._current_coalition_value = content.coalition_value
            self._is_done = True
            print(f"{self.aid} is done searching.")
            return

        elif isinstance(content, RefusalMessage):
            if self.aid == content.agent_id:
                for i, agent in enumerate(content.refused_agents):
                    self._available_agents.update({agent: False})
                    if agent == content.agent_id and self.request_count > 0:
                        self.request_count = self.request_count - 1
                        if self.request_count == 0:
                            self._is_done = True
                            print(f"{self.aid} is done searching.")
            return

        else:
            print(f"{self.aid}: The message with the content {content} has a wrong type.")
        return

    def calculate_coalition_value(self, foreign_coordinate, foreign_power):
        """
        Calculates the coalition value of the possibly new coalition to compare it to the current value.
        :param foreign_coordinate: The coordinate of the requesting agent.
        :param foreign_power: The power generation of the requesting agent.
        :return: Returns the new coalition value.
        """

        coalition_agent_distances = []
        coalition_agent_power_outputs = 0

        for i, agent in enumerate(self._current_coalition_agents):
            coalition_agent_distances.append(self._current_coalition_agents[i].location_coordinate)
            coalition_agent_power_outputs = coalition_agent_power_outputs + agent.expected_power_generation
        coalition_agent_distances.append(foreign_coordinate)
        coalition_agent_power_outputs.append(foreign_power)

        distance_value = self.euclidean_coalition_distance(coalition_agent_distances)

        power_value = self.calculate_power_value(coalition_agent_power_outputs / len(coalition_agent_power_outputs))

        return distance_value * power_value

    def calculate_power_value(self, power_output):
        """
        This is a Gauss deviation function to incentivise that low and high power generating wind turbines come together
        :param power_output: The expected power output of the coalition in a ratio to 3000 kW
        :return: Returns the new power value
        """
        return (1 / (self.POWER_FUNCTION_SIGMA * np.sqrt(2 * np.pi))
                * np.exp(-0.5 * ((power_output - self.POWER_FUNCTION_MU) / self.POWER_FUNCTION_SIGMA) ** 2))\
                * self.POWER_AMPLITUDE + self.POWER_FUNCTION_HEIGHT

    def euclidean_coalition_distance(self, coalition_coordinates):
        """
        Calculates the average distance of all coordinates in this coalition
        :param coalition_coordinates: These are all coordinates of a coalition in tuples
        :return: Returns the average distance
        """
        sum_distances = 0

        # Adds all weights (distances) of the edges in a coalition graph
        for i, coord_a in enumerate(coalition_coordinates):
            for j, coord_b in enumerate(coalition_coordinates):
                if i < j:
                    x1, y1 = coord_a
                    x2, y2 = coord_b
                    sum_distances = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        # Calculates the amount of edges in a coalition graph
        n = len(coalition_coordinates)
        amount_edges = (n*(n-1))/2

        # Returns the average of distances in a coalition
        return sum_distances / amount_edges

    def set_available_agents(self, agents):
        """
        Setter method to update all available agents. Converts the agents class into the agent_id String.
        :param agents: Sets these agents.
        """
        self._neighbor_agents = agents
        for i, agent in enumerate(agents):
            self._available_agents.update({agent.aid: True})
        self._available_agents.update({self.aid: False})
