"""
The agent is used to generate an agent to decide whether meachine or part to operate.
"""
import random
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
        self.machines = self.machine.machines

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
        return self.firstInFirstOut()
        # return self.firstInLastOut()

    @staticmethod
    def firstInFirstOut() -> int:
        return 0

    def firstInLastOut(self) -> int:
        return self.pre_buffer.getLength() - 1


class Machine2MachineAgent(Agent):
    def __init__(self, self_machine):
        super().__init__(self_machine)
        self.buffers = [m.pre_buffer for m in self.machines]
        self.decide_rules = self.shortestProcessingTime

    def decide(self) -> int:
        """define which machine to be choosen."""
        part: Part = self.machine.operate_part
        now_time_dict = part.getNowTimeDict()
        return self.decide_rules(now_time_dict)

    @staticmethod
    def shortestProcessingTime(time_dict) -> int:
        """SMPT: Selects the machine with the smallest processing time of the operation."""
        min_value_item = min(time_dict.items(), key=lambda x: x[1])
        # index in dict begin from 1 but need to begin from 0.
        return min_value_item[0] - 1

    def shortestBuffer(self, time_dict) -> int:
        """NINQ Selects the machine with the smallest number of jobs in the buffer. """
        available_list = list(m-1 for m in time_dict)
        length_of_buffer = [self.buffers[m_id].getLength() for m_id in available_list]
        min_length = min(length_of_buffer)
        min_index = length_of_buffer.index(min_length)

        return available_list[min_index]

    def smallestWorkload(self, time_dict) -> int:
        """WINQ Selects the machine with the smallest workload. """
        available_list = list(m - 1 for m in time_dict)
        utilization_list = [self.machines[m_id].getUtilization() for m_id in available_list]
        min_length = min(utilization_list)
        min_index = utilization_list.index(min_length)

        return available_list[min_index]

    @staticmethod
    def randomChooser(time_dict) -> int:
        """Randomly chooses"""
        available_list = list(m for m in time_dict)
        result = random.choice(available_list)
        return result - 1


class WarseHouseAgent(Machine2MachineAgent):
    def __init__(self, self_machine):
        super().__init__(self_machine)

    def decideByPart(self, part: Part) -> int:
        """define which machine to be choosen."""
        now_time_dict = part.getNowTimeDict()
        return self.shortestProcessingTime(now_time_dict)
