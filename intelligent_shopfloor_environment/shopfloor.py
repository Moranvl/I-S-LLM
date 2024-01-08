"""
The shopfloor Class is used to generate a shopfloor by files.
The shopfloor is the basic of this environment.
"""
from intelligent_shopfloor_environment.machine import Machine, WareHouse
from intelligent_shopfloor_environment.timer import TimeController
from intelligent_shopfloor_environment.part import Part


class ShopFloor:
    """
    The Shopfloor class.
    """
    def __init__(self, init_file: str = ""):
        """Initialize the Shopfloor class."""
        # Save the initial parameters.
        self.init_file: str = init_file

        # Initialize the variables.
        self.machines: tuple or None = None
        self.generate_warehouse: WareHouse or None = None
        self.timer = TimeController(self)

        # Initialize the Shopfloor.
        self. initialize_shopfloor()

    # region Initialization
    def initialize_shopfloor(self) -> None:
        """Initialize the Shopfloor class"""
        machine_information, part_information = self.file2environment(self.init_file)
        self.generate_warehouse = WareHouse(part_template=self.generateParts(part_information))
        self.machines = self.generate_machines(machine_information)

    @staticmethod
    def generate_machines(machine_len: int) -> tuple[Machine, ...]:
        """
        Generate the shopfloor from files.
        - machine_len: It should be an integer.
        :return:
        - machine_tuple: tuple of machines.
        """
        return tuple(Machine(machine_id=i) for i in range(1, machine_len+1))

    @staticmethod
    def generateParts(part_information: list[tuple[dict]]):
        part_template = [Part(process_tuple=info_tuple) for info_tuple in part_information]
        return part_template

    def file2environment(self, filename: str) -> tuple[int, list[tuple[dict]]]:
        """
        - filename: the path or the name of file which include the infomation of shopfloor
        :return:
        - machine_information: The length of the machines.
        - part_infomation: The information of parts.[({}, {}, {}), (), ()]
        """
        part_infomation = list()
        machine_information = 0
        return machine_information, part_infomation

    # endregion

    def reset(self) -> None:
        """Reset the Shopfloor."""
        self.generate_warehouse.reset()
        [m.reset() for m in self.machines]
        self.timer.reset()

    def run(self):
        """
        Run shopfloor.
        :return: None
        """
        over = False
        self.timer.start()
        while over := self.isOver():
            self.timer.tickTick()

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

    def isOver(self) -> bool:
        over_list = [m.isOver() for m in self.machines]
        over_list.append(self.generate_warehouse.isOver())
        return all(over_list)
