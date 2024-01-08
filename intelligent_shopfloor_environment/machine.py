"""
The mechine class is used to generate a meachine to operate and process part.
"""
from typing import override
from intelligent_shopfloor_environment.part import Part, PartBuffer
from intelligent_shopfloor_environment.agent import Agent
from intelligent_shopfloor_environment.timer import TimeController


class Machine:
    """Machine class"""

    def __init__(
            self,
            timer: TimeController,
            *,
            machine_id: int = -1,
    ):
        self._id = machine_id
        self.pre_buffe: PartBuffer = PartBuffer()
        self.agent_buffer2machine: Agent = Agent(self)
        self.agent_machine2machine: Agent = Agent(self)
        self.timer = timer
        # Variables to save the state.
        self.operate_part: Part or None = None
        self.part_over_time: int = 0

    def onTickTick(self, new_time: int):
        """
        Tick tick when the time is change.
        Dispatch over part to other machine or store.
        """
        if self.isMachineNeedDispatch(new_time):
            self.dispatchOverPart()

    def dispatchOverPart(self):
        pass

    def onTickTickSecond(self, new_time: int):
        """
        Tick tick when the time is change.
        Choose a part to machine.
        """
        if self.isBufferNeedChoosen():
            self.choosePart2Machine()

    def choosePart2Machine(self):
        pass

    def needingTime(self) -> int:
        """
        Compute the next time step.
        If machine is free, return empty, else return the needing time.
        :return:
        """
        if self.isMachineFree():
            return 0
        else:
            return self.part_over_time - self.timer.time

    def processes(self):
        """operate the part"""
        pass

    def reset(self):
        pass

    def partIn(self, part: Part):
        """input the part"""
        self.pre_buffe.addPart(part)

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

    def isPartProcessOver(self, t) -> bool:
        return t >= self.part_over_time

    def isMachineNeedDispatch(self, now_time: int) -> bool:
        machine_buzy = not self.isMachineFree()
        part_process_over = self.isPartProcessOver(now_time)

        return machine_buzy and part_process_over

    def isBufferNeedChoosen(self) -> bool:
        buffer_empty = self.pre_buffe.isEmpty()
        machine_busy = not self.isMachineFree()
        # return (not buffer_empty) and (not machine_busy)
        return not (buffer_empty and machine_busy)

    # endregion


class WareHouse(Machine):
    """Used to generate parts to be processed."""

    def __init__(self, part_template: list[Part]):
        super().__init__()
        self.part_template = part_template

    @override
    def onTickTick(self):
        pass
