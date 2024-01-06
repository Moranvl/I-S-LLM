"""
The mechine class is used to generate a meachine to operate and process part.
"""


class Machine:
    """Machine class"""
    def __init__(
            self, *,
            machine_type: int = -1, machine_id: int = 0
    ):
        self._type = machine_type
        self._id = machine_id
        self.part_list = []

    def operate(self):
        """operate the part"""
        pass

    def part_in(self):
        """input the part"""
        pass

    def part_out(self):
        """output the part"""
        pass
