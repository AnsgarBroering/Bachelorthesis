from dataclasses import dataclass

@dataclass
class RequestMessage:
    """
    An agent sends a request to join a coalition.
    """

    agent_id: str
    coordinate: []
    power_profile: float

    def __init__(self, agent_id, coordinate, power_profile):
        self.agent_id = agent_id
        self.coordinate = coordinate
        self.power_profile = power_profile

@dataclass
class AdmissionMessage:
    """
    An agent which is allowed to join the coalition gets an admission message.
    All agents in the coalition gets updated.
    """
    agent_id: str
    coalition_value: float

    def __init__(self, agent_id, coalition_value):
        self.agent_id = agent_id
        self.coalition_value = coalition_value

@dataclass
class RefusalMessage:
    """
    An agent which isn't allowed to join the coalition gets a refusal message.
    All agents in the coalition also get the information of the refused agent.
    """

    agent_id: str
    refused_agents: []

    def __init__(self, agent_id, refused_agents):
        self.agent_id = agent_id
        self.refused_agents = refused_agents

@dataclass
class EvaluationMessage:
    """
    This message is send to one agent who evaluates all incoming data
    """
    agent_id: str
    coalition_id: str
    coalition_agents: []
    coalition_distance: float
    coalition_power: float
    coalition_value: float

    def __init__(self, agent_id, coalition_id, coalition_agents, coalition_distance, coalition_power, coalition_value):
        self.agent_id = agent_id
        self.coalition_id = coalition_id
        self.coalition_agents = coalition_agents
        self.coalition_distance = coalition_distance
        self.coalition_power = coalition_power
        self.coalition_value = coalition_value