"""
the agents based on llm.
"""
from intelligent_shopfloor_environment.agent import Agent, Buffer2MachineAgent, Machine2MachineAgent
from intelligent_shopfloor_environment.part import Part, PartBuffer
from configparser import ConfigParser
from openai import OpenAI
from http import HTTPStatus
import dashscope
from dashscope import Generation
from dashscope.api_entities.dashscope_response import Role


class LlmAgent:
    def __init__(self, model_name="qwen"):
        self.cf = ConfigParser()
        self.cf.read('config.ini', encoding='utf-8')

        self.model_name = model_name
        if model_name == "gpt":
            self.model = self.cf.get('gpt', 'model')
            api_key = self.cf.get('gpt', 'api_key')
            self.client = OpenAI(api_key=api_key)
            self.temperature = self.cf.getfloat('gpt', 'temperature')
        elif model_name == "qwen":
            self.temperature = self.cf.getfloat('qwen', 'temperature')
            api_key = self.cf.get('qwen', 'api_key')
            dashscope.api_key = api_key
            self.model = Generation.Models.qwen_max
        else:
            raise ValueError("Error Model Name")

        self.prompt = """
        Enter your prompts.
        """

    def gpt_text_generation(self, system_prompt: str, user_prompt: str, temperature=1.0):
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

    @staticmethod
    def qwen_text_generation(system_prompt: str, user_prompt: str, temperature=1.0):
        messages = [
            {'role': Role.SYSTEM, 'content': system_prompt},
            {'role': Role.USER, 'content': user_prompt}
        ]
        response = Generation.call(
            Generation.Models.qwen_max,
            messages=messages,
            result_format='message',  # set the result to be "message" format.
            stream=False,
            incremental_output=False,  # get streaming output incrementally
            temperature=temperature
        )
        full_content = ''
        if response.status_code == HTTPStatus.OK:
            full_content += response.output.choices[0]['message']['content']
        else:
            print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                response.request_id, response.status_code,
                response.code, response.message
            ))
        return full_content

    def text_generation(self, system_prompt: str, user_prompt: str):
        if self.model_name == "gpt":
            return self.gpt_text_generation(system_prompt, user_prompt, self.temperature)
        elif self.model_name == "qwen":
            return self.qwen_text_generation(system_prompt, user_prompt, self.temperature)
        else:
            raise ValueError("Error Model Name")


class Buffer2MachineAgentLLM(Buffer2MachineAgent, LlmAgent):
    def __init__(self, self_machine, model_name="qwen"):
        Buffer2MachineAgent.__init__(self, self_machine)
        LlmAgent.__init__(self, model_name=model_name)

        self.machines = self.machine.machines
        self.prompt = """
        Enter your prompts.
        """

    def decide(self) -> int:
        return self.firstInFirstOut()

    def getBufferLength(self):
        return self.pre_buffer.getLength()


class Machine2MachineAgentLLM(Machine2MachineAgent, LlmAgent):
    def __init__(self, self_machine, model_name="qwen"):
        Machine2MachineAgent.__init__(self, self_machine)
        LlmAgent.__init__(self, model_name)

        self.machines = self.machine.machines
        with open("intelligent_shopfloor_environment/prompts/machine_choosen_prompt.txt") as f:
            self.machine_choose_prompt = f.read()
        with open("intelligent_shopfloor_environment/prompts/machine_fitter_prompt.txt") as f:
            self.machine_fitter_prompt = f.read()

    def decide(self) -> int:
        part: Part = self.machine.operate_part
        machine_list = part.getProcessingMachineList()

        len_machine_list = len(machine_list)
        if len_machine_list == 1:
            return machine_list[0] - 1
        elif len_machine_list > 1:
            bidding_documents = [
                self.machines[machine_id - 1].generateDocument(part)
                for machine_id in machine_list
            ]
            usr_prompt = self.generateUserPrompt(bidding_documents, part)
            decision_form_llm = self.text_generation(system_prompt=self.machine_choose_prompt, user_prompt=usr_prompt)
            decision = self.generateDecision(decision_form_llm, machine_list)
            return decision
        else:
            raise ValueError(f"The length of machine list is wrong {len_machine_list}")

    def generateUserPrompt(self, documents, part: Part):
        now_index, length = part.getOperationIndex()
        prompt = f"""# Job information:
This job still needs <{length-now_index}> operations and the number of total operation is {length}.
The bidding documents from available machine is:
# Bidding documents from available machine:"""
        for doc in documents:
            prompt += "\n"
            prompt += doc
        return prompt

    def generateDecision(self, decision_form_llm, machine_list) -> int:
        temp_machine_index_plus = self.text_generation(
            system_prompt=self.machine_fitter_prompt, user_prompt=decision_form_llm
        )
        machine_index_plus = int(temp_machine_index_plus)
        assert machine_index_plus in machine_list
        return machine_index_plus - 1


class WarseHouseAgentLLM(Machine2MachineAgent):
    def __init__(self, self_machine):
        super().__init__(self_machine)

    def decideByPart(self, part: Part) -> int:
        """define which machine to be choosen."""
        now_time_dict = part.getNowTimeDict()
        return self.shortestProcessingTime(now_time_dict)
