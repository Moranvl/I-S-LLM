"""
The shopfloor Class is used to generate a shopfloor by files.
The shopfloor is the basic of this environment.
"""
from intelligent_shopfloor_environment.machine import Machine
from intelligent_shopfloor_environment.timer import TimeController


class ShopFloor:
    """
    The Shopfloor class.
    """
    def __init__(self):
        """Initialize the Shopfloor class."""
        self.machines: tuple or None = None
        self.timer = TimeController()

    def generate_shopfloor(self, machine_list: list):
        """
        Generate the shopfloor from files.
        - machine_list: It should be a list, the index represents the id of machine,
                        and the number represents the number of machine.
        """
        self.machines = tuple(
            tuple(
                Machine(machine_type=m_type, machine_id=m_id)
                for m_id in range(m_num)
            )
            for m_type, m_num in enumerate(machine_list)
        )
