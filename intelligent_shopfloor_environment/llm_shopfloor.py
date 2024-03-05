"""
This shopfloor is extended from shopfloor.
"""
from intelligent_shopfloor_environment.shopfloor import ShopFloor
from intelligent_shopfloor_environment.agent import Agent
from intelligent_shopfloor_environment.llm_agent import (
    Buffer2MachineAgentLLM, Machine2MachineAgentLLM, WarseHouseAgentLLM
)


class ShopfloorLLM(ShopFloor):
    def __init__(self, init_file: str = "./dataset"):
        super().__init__(init_file)

    def initialize_agents(self) -> None:
        """initial the agents"""
        for m in self.machines:
            m.defineAgent(
                buffer2machine_agent=Buffer2MachineAgentLLM(m), machine2machine_agent=Machine2MachineAgentLLM(m, "qwen")
            )
        self.generate_warehouse.defineAgent(
            buffer2machine_agent=Agent(self.generate_warehouse),
            machine2machine_agent=WarseHouseAgentLLM(self.generate_warehouse),
        )
