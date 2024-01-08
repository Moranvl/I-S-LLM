"""
The agent is used to generate an agent to decide whether meachine or part to operate.
"""
from intelligent_shopfloor_environment.machine import Machine, WareHouse


class Agent:
    """
    Agent class for decision.
    """

    def __init__(
            self, self_machine: Machine or WareHouse
    ):
        self.machine = self_machine


class Buffer2MachineAgent(Agent):
    pass


class Machine2MachineAgent(Agent):
    pass
