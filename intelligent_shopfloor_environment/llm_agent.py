"""
the agents based on llm.
"""
from intelligent_shopfloor_environment.agent import Agent, Buffer2MachineAgent, Machine2MachineAgent
from intelligent_shopfloor_environment.part import Part, PartBuffer


class Buffer2MachineAgentLLM(Buffer2MachineAgent):
    def __init__(self, self_machine):
        super().__init__(self_machine)
        self.prompt = """
        Enter your prompts.
        """

    def decide(self) -> int:
        pass

    def getBufferLength(self):
        return self.pre_buffer.getLength()


class Machine2MachineAgentLLM(Machine2MachineAgent):
    def __init__(self, self_machine):
        super().__init__(self_machine)
        self.prompt = """
        Enter your prompts.
        """

    def decide(self) -> int:
        part: Part = self.machine.operate_part
        return 0

    @staticmethod
    def getAvailableMachine(part: Part):
        now_time_dict = part.getNowTimeDict()
        # return (m_id for m_id, m_time in now_time_dict.items())
        return tuple(m_id for m_id in now_time_dict)


