import asyncio
from mango import Agent
from mango.messages.message import Performatives
from mango.util.scheduling import InstantScheduledProcessTask
from mango.util.clock import AsyncioClock, ExternalClock
import math
import random
from CodecMessages import RequestMessage, AdmissionMessage, RefusalMessage

class WindTurbineAgent(Agent):

    _container = 0
    _container_address = []
    _location_coordinate = [0, 0]
    _expected_power_generation = 0
    _current_coalition_value = 0
    _current_coalition_agents = []
    _neighbor_agents = []           # classes of all neighboring agents
    _available_agents = {}          # agent id and their availability
    _depleted_request_pool = False
    _is_done = False
    request_count = 0
    DISTANCE_WEIGHT = 0.7
    POWER_WEIGHT = 0.3
    RATED_CAPACITY = 2500

    def __init__(self, container, address, coordinate, power):
        super().__init__(container)
        self._container = container
        self._container_address = address
        self._location_coordinate = coordinate
        self._expected_power_generation = power
        self._current_coalition_agents.append(self.aid)
        print(f"My id is {self.aid}.")

    async def initiate_requests(self, request_count, delay_in_seconds):
        self.request_count = request_count
        self.schedule_timestamp_task(coroutine=self.start_requests(),
                                     timestamp=self.current_timestamp + delay_in_seconds)
        return

    async def start_requests(self):
        # Checks if any agents are still available
        available_agents = [key for key, value in self._available_agents.items() if value]
        # If any agent is available a message is sent to it
        if available_agents:
            request_receiver = random.choice(available_agents)
            print(f"{self.aid} started sending a message.")
            message_content = RequestMessage(self.aid, self._location_coordinate, self._expected_power_generation)
            await self.send_message(message_content, self._container_address, request_receiver)
            await asyncio.sleep(10)
        else:
            self._depleted_request_pool = True
        return


    async def handle_message(self, content, meta):
        """
        When a message is received it gets handled here. It can be a
        """
        print(f"{self.aid} has received a message.")
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

        # ToDo: Currently all coalition agents are set on FALSE
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

        coalition_agent_distances = []

        for i in self._current_coalition_agents:
            coalition_agent_distances.append(self._current_coalition_agents[i].location_coordinate)
        coalition_agent_distances.append(foreign_coordinate)

        distance_value = self.euclidean_coalition_distance(coalition_agent_distances)

        power_value = foreign_power / self.RATED_CAPACITY

        return distance_value * self.DISTANCE_WEIGHT + power_value * self.POWER_WEIGHT

    def euclidean_coalition_distance(self, coalition_coordinates):
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
        self._neighbor_agents = agents
        for i, agent in enumerate(agents):
            self._available_agents.update({agent.aid: True})
        self._available_agents.update({self.aid: False})
        return
