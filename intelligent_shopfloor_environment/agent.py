"""
The agent is used to generate an agent to decide whether meachine or part to operate.
"""
from intelligent_shopfloor_environment.part import Part, PartBuffer


class Agent:
    """
    Agent class for decision.
    """

    def __init__(
            self, self_machine,
    ):
        """
        Initialize the agent.
        :param self_machine: Machine or Warehouse
        """
        self.machine = self_machine

    def decide(self) -> int:
        """
        Deside wheather machine or part to be choosen.
        :return: the index of diciusion machine.
        """
        raise ValueError("Deside not defined")


class Buffer2MachineAgent(Agent):
    def __init__(self, self_machine):
        super().__init__(self_machine)
        self.pre_buffer = self.machine.pre_buffer

    def decide(self) -> int:
        # return self.firstInFirstOut()
        return self.firstInLastOut()

    @staticmethod
    def firstInFirstOut() -> int:
        return 0

    def firstInLastOut(self) -> int:
        return self.pre_buffer.getLength() - 1


class Machine2MachineAgent(Agent):
    def __init__(self, self_machine):
        super().__init__(self_machine)

    def decide(self) -> int:
        """define which machine to be choosen."""
        part: Part = self.machine.operate_part
        now_time_dict = part.getNowTimeDict()
        return self.shortestProcessingTime(now_time_dict)

    @staticmethod
    def shortestProcessingTime(time_dict) -> int:
        """SPT"""
        min_value_item = min(time_dict.items(), key=lambda x: x[1])
        # index in dict begin from 1 but need to begin from 0.
        return min_value_item[0] - 1


class WarseHouseAgent(Machine2MachineAgent):
    def __init__(self, self_machine):
        super().__init__(self_machine)

    def decideByPart(self, part: Part) -> int:
        """define which machine to be choosen."""
        now_time_dict = part.getNowTimeDict()
        return self.shortestProcessingTime(now_time_dict)
