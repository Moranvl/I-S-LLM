"""
The mechine class is used to generate a meachine to operate and process part.
"""
from intelligent_shopfloor_environment.part import Part, PartBuffer, OverPartBuffer
from intelligent_shopfloor_environment.agent import Agent
from intelligent_shopfloor_environment.timer import TimeController


class Machine:
    """Machine class"""

    def __init__(
            self,
            timer: TimeController,
            over_part_buffer: OverPartBuffer,
            *,
            machine_id: int = -1,
    ):
        self._id = machine_id
        self.pre_buffer: PartBuffer = PartBuffer()

        self.agent_buffer2machine: Agent or None = None
        self.agent_machine2machine: Agent or None = None

        # get the pointer of the machines.
        self.machines: tuple[Machine] or None = None
        # get the pointer of the over part buffer
        self.over_part_buffer: OverPartBuffer = over_part_buffer
        # get the pointer of the timer
        self.timer = timer

        # Variables to save the state.
        self.operate_part: Part or None = None
        self.part_over_time: int = 0

    def defineMachine(self, machines: tuple):
        """get the machines after the machine is generated."""
        self.machines = machines
        self.agent_buffer2machine: Agent or None = None
        self.agent_buffer2machine: Agent or None = None

    def defineAgent(self, buffer2machine_agent: Agent, machine2machine_agent: Agent) -> None:
        """define the agent."""
        self.agent_buffer2machine = buffer2machine_agent
        self.agent_machine2machine = machine2machine_agent

    # region First TickTick
    def onTickTick(self, new_time: int):
        """
        Tick tick when the time is change.
        Dispatch over part to other machine or store.
        """
        if self.isMachineNeedDispatch(new_time):
            self.dispatchOverPart()

    def dispatchOverPart(self):
        part = self.operate_part
        part.process()
        if part.isOver():
            self.over_part_buffer.addPart(part)
        else:
            # Add part to other machine.
            index = self.agent_machine2machine.decide()
            self.machines[index].partIn(part)
        # Clear the part.
        self.operate_part = None

    # endregion

    # region Second TickTick
    def onTickTickSecond(self, new_time: int):
        """
        Tick tick when the time is change.
        Choose a part to machine.
        """
        if self.isBufferNeedChoosen():
            self.choosePart2Machine(new_time)

    def choosePart2Machine(self, new_time: int) -> None:
        index = self.agent_buffer2machine.decide()
        part = self.pre_buffer.takePart(index)

        #
        self.part_over_time = new_time + part.getProcessingTime(self._id)
        # assign part to the machine.
        self.operate_part = part

    # endregion

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

    def reset(self):
        pass

    def partIn(self, part: Part):
        """input the part"""
        self.pre_buffer.addPart(part)

    # region Judgment
    def isOver(self) -> bool:
        """
        check if any part is processing or not to be processed.
        :return: bool
        """
        buffer_empty = self.pre_buffer.isEmpty()
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
        buffer_empty = self.pre_buffer.isEmpty()
        machine_busy = not self.isMachineFree()
        # return (not buffer_empty) and (not machine_busy)
        return not (buffer_empty or machine_busy)

    # endregion


class WareHouse(Machine):
    """Used to generate parts to be processed."""

    def __init__(
            self,
            part_template: list[Part],
            timer: TimeController,
            over_part_buffer: OverPartBuffer,
    ):
        super().__init__(timer, over_part_buffer=over_part_buffer)
        [self.pre_buffer.addPart(part) for part in part_template]

    def onTickTick(self, new_time: int):
        """
        Dispatching the part to the first machine.
        @override
        :param new_time: time for now.
        :return:
        """
        while buffer_not_empty := not self.pre_buffer.isEmpty():
            self.dispatchParts()

    def dispatchParts(self) -> None:
        part = self.takePartFromBuffer()
        part.process()
        index = self.agent_machine2machine.decideByPart(part)
        self.machines[index].partIn(part)

    def takePartFromBuffer(self) -> Part:
        return self.pre_buffer.takePart(0)

    def onTickTickSecond(self, new_time: int):
        """
        Warehouse need not be called.
        @override
        :param new_time: int
        :return:
        """
        pass
