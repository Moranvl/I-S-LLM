"""
The shop floor Class is used to generate a shopfloor by files.
The shop floor is the basic of this environment.
"""
import numpy as np

from intelligent_shopfloor_environment.machine import Machine, WareHouse
from intelligent_shopfloor_environment.timer import TimeController
from intelligent_shopfloor_environment.part import Part, OverPartBuffer
from intelligent_shopfloor_environment.agent import Agent, Buffer2MachineAgent, Machine2MachineAgent, WarseHouseAgent
from intelligent_shopfloor_environment.utils import analysisDataFile


class ShopFloor:
    """
    The Shop floor class.
    """

    def __init__(
            self, init_file: str = "./dataset",
    ):
        """
        Initialize the Shop-floor class.
        Dataset information should contain "dataset_dir", "dataset_name", "file_name".
        """
        # Save the initial parameters.
        self.init_file: str = init_file

        # Initialize the variables.
        self.machines: tuple[Machine] or None = None
        self.generate_warehouse: WareHouse or None = None
        self.over_parts: OverPartBuffer = OverPartBuffer()
        self.timer = TimeController(self)

        # Initialize the Shop-floor.
        self.initialize_shopfloor()
        # Define shopfloor of the machines
        self.define_shopfloor()
        # Initialize the agents.
        self.initialize_agents()

    # region Initialization
    def initialize_shopfloor(self) -> None:
        """Initialize the Shop-floor class"""
        machine_information, part_information = self.file2environment(self.init_file)
        self.generate_warehouse = WareHouse(
            timer=self.timer, part_template=self.generateParts(part_information), over_part_buffer=self.over_parts
        )
        # initialize the machines
        self.machines = self.generate_machines(machine_information)
        [m.defineMachine(self.machines) for m in self.machines]
        self.generate_warehouse.defineMachine(self.machines)

        # Initialize the TimeController
        self.timer.attach(self.generate_warehouse)
        [self.timer.attach(m) for m in self.machines]

        # after initialization the timer
        self.timer.lazy_init()

    def initialize_agents(self) -> None:
        """initial the agents"""
        for m in self.machines:
            m.defineAgent(buffer2machine_agent=Buffer2MachineAgent(m), machine2machine_agent=Machine2MachineAgent(m))
        self.generate_warehouse.defineAgent(
            buffer2machine_agent=Agent(self.generate_warehouse),
            machine2machine_agent=WarseHouseAgent(self.generate_warehouse),
        )

    def define_shopfloor(self) -> None:
        """define the shopfloor from machines"""
        for m in self.machines:
            m.defineShopfloor(self)
        self.generate_warehouse.defineShopfloor(self)

    def generate_machines(self, machine_len: int) -> tuple[Machine, ...]:
        """
        Generate the shopfloor from files.
        - machine_len: It should be an integer.
        :return:
        - machine_tuple: tuple of machines.
        """
        return tuple(
            Machine(timer=self.timer, over_part_buffer=self.over_parts, machine_id=i)
            for i in range(1, machine_len + 1)
        )

    @staticmethod
    def generateParts(part_information: list[tuple[dict]]):
        part_template = [
            Part(index=index, process_tuple=info_tuple)
            for index, info_tuple in enumerate(part_information)
        ]
        return part_template

    @staticmethod
    def file2environment(filename: str) -> tuple[int, list[tuple[dict]]]:
        """
        - filename: the path or the name of file which include the infomation of shopfloor
        :return:
        - machine_information: The length of the machines.
        - part_infomation: The information of parts.[({}, {}, {}), (), ()]
        """
        # Need to judge if any part's length is 0 or even negative integer number.
        machine_information, part_infomation = analysisDataFile(filename)
        return machine_information, part_infomation

    # endregion

    def reset(self) -> None:
        """Reset the Shopfloor."""
        self.generate_warehouse.reset()
        [m.reset() for m in self.machines]
        self.timer.reset()
        self.over_parts.reset()

    def run(self):
        """
        Run shopfloor.
        :return: None
        """
        over = False
        self.timer.start()
        while not (over := self.isOver()):
            self.timer.tickTick()
        print(f"End time step: {self.timer.time}")

    def plotData(self, figsize, save_dir, plot_adjust=None, need_text=True):
        self.over_parts.plotData(
            len(self.machines), end_time=self.timer.time, figsize=figsize, save_dir=save_dir, plot_adjust=plot_adjust,
            need_text=need_text
        )

    # region Get Information
    def getNextTimeStep(self) -> int:
        """
        compute next time step.
        If needing time is all 0, the shopfloor is over.
        :return:
        """
        needing_time = set(m.needingTime() for m in self.machines)
        if 0 in needing_time:
            needing_time.remove(0)
        next_time_step = min(needing_time) + self.timer.time
        return next_time_step

    def getMachineNum(self) -> int:
        return len(self.machines)

    def getTime(self) -> int:
        return self.timer.time

    def getUtilizationMeanAndVariance(self) -> tuple[float, ...]:
        utilization_list = np.array([m.getUtilization() for m in self.machines])
        return np.mean(utilization_list), np.var(utilization_list, ddof=1)

    def getUtilizationVariance(self) -> float:
        _, variance = self.getUtilizationMeanAndVariance()
        return variance

    # endregion

    def isOver(self) -> bool:
        over_list = [m.isOver() for m in self.machines]
        over_list.append(self.generate_warehouse.isOver())
        return all(over_list)

