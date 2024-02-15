"""
the agents based on llm.
"""
from intelligent_shopfloor_environment.agent import Agent, Buffer2MachineAgent, Machine2MachineAgent
from intelligent_shopfloor_environment.part import Part, PartBuffer
from configparser import ConfigParser
from openai import OpenAI


class LlmAgent:
    def __init__(self):
        self.cf = ConfigParser()
        self.cf.read('config.ini', encoding='utf-8')

        self.api_key = self.cf.get('gpt', 'api_key')
        self.model = self.cf.get('gpt', 'model')
        self.temperature = self.cf.getfloat('gpt', 'temperature')

        self.client = OpenAI()

    def text_generation(self, system_prompt: str, user_prompt: str, temperature=1.0):
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system",
                 "content": system_prompt},
                {"role": "user", "content": "user_prompt"}
            ],
            temperature=self.temperature
        )

        return completion.choices[0].message


class Buffer2MachineAgentLLM(Buffer2MachineAgent):
    def __init__(self, self_machine):
        super().__init__(self_machine)
        self.machines = self.machine.machines
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
        self.machines = self.machine.machines
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
