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

    def deside(self) -> int:
        """
        Deside wheather machine or part to be choosen.
        :return: the index of diciusion machine.
        """
        return 0


class Buffer2MachineAgent(Agent):
    pass


class Machine2MachineAgent(Agent):
    def __init__(self, self_machine: Machine or WareHouse):
        super().__init__(self_machine)
