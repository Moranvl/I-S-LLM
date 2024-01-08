"""
The mechine class is used to generate a meachine to operate and process part.
"""
from typing import override
from intelligent_shopfloor_environment.part import Part, PartBuffer


class Machine:
    """Machine class"""

    def __init__(
            self, *,
            machine_id: int = -1
    ):
        self._id = machine_id
        self.pre_buffe: PartBuffer = PartBuffer()
        self.operate_part: Part or None = None

    def onTickTick(self, new_time: int):
        """Tick tick when the time is change"""
        pass

    def needingTime(self) -> int:
        """
        Compute the next time step.
        If machine is free, return empty, else return the needing time.
        :return:
        """
        pass

    def processes(self):
        """operate the part"""
        pass

    def reset(self):
        pass

    def part_in(self):
        """input the part"""
        pass

    def part_out(self):
        """output the part"""
        pass

    # region judgment
    def isOver(self) -> bool:
        """
        check if any part is processing or not to be processed.
        :return: bool
        """
        buffer_empty = self.pre_buffe.isEmpty()
        machine_free = self.isMachineFree()
        return buffer_empty and machine_free

    def isMachineFree(self) -> bool:
        return self.operate_part is None

    # endregion


class WareHouse(Machine):
    """Used to generate parts to be processed."""

    def __init__(self, part_template: list[Part]):
        super().__init__()
        self.part_template = part_template

    @override
    def onTickTick(self):
        pass
