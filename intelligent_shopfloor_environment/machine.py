"""
The mechine class is used to generate a meachine to operate and process part.
"""
from copy import deepcopy
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
        # Utilization
        self.accumulate_work_time: int = 0
        self.part_start_time: int = 0

    # region Definition
    def defineMachine(self, machines: tuple):
        """get the machines after the machine is generated."""
        self.machines = machines
        self.agent_buffer2machine: Agent or None = None
        self.agent_buffer2machine: Agent or None = None

    def defineAgent(self, buffer2machine_agent: Agent, machine2machine_agent: Agent) -> None:
        """define the agent."""
        self.agent_buffer2machine = buffer2machine_agent
        self.agent_machine2machine = machine2machine_agent

    # endregion

    # region First TickTick
    def onTickTick(self, new_time: int):
        """
        Tick tick when the time is change.
        Dispatch over part to other machine or store.
        """
        if self.isMachineNeedDispatch(new_time):
            self.dispatchOverPart(new_time)

    def dispatchOverPart(self, new_time: int):
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
        part.saveEndTime(new_time)
        # Something else to be processed after processing.
        self.accumulate_work_time += new_time - self.part_start_time

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
        """part in machine"""
        index = self.agent_buffer2machine.decide()
        part = self.pre_buffer.takePart(index)

        self.part_over_time = new_time + part.getProcessingTime(self._id)
        # assign part to the machine.
        self.operate_part = part
        # Something else to be processed before processing.
        (part.saveMachineID(self._id), part.saveStartTime(new_time))
        self.part_start_time = new_time

    # endregion

    # region Get Information
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

    def getUtilization(self) -> float:
        t = self.timer.time
        if self.isMachineFree():
            return self.accumulate_work_time / t
        else:
            return (self.accumulate_work_time - self.part_start_time) / t + 1

    # endregion

    def reset(self):
        self.pre_buffer.reset()

        # Variables to save the state.
        self.operate_part = None
        self.part_over_time = 0
        # Utilization
        self.accumulate_work_time = 0
        self.part_start_time = 0

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

    # region Servering Agent
    def generateDocument(self, part: Part):
        part_need_time = part.getProcessingTime(self._id)
        free_or_busy = ""
        eariliest_time = 0
        if self.isMachineFree():
            free_or_busy += "<free>."
            eariliest_time += self.timer.time + part_need_time
        else:
            free_or_busy += f"<busy>, and I still need <{self.needingTime()}> time step to over this order."
            eariliest_time += self.part_over_time + part_need_time
        completion_rate_operations, completion_rate_jobs = self.pre_buffer.getCompletionRate()

        prompt = f"""# Machine: {self._id}
The state of my machine is {free_or_busy}
The length of my buffer is {self.pre_buffer.getLength()}.
My history utilization is <{self.getUtilization()}>.
My average completion rate of operation is <{completion_rate_operations}>.
My average completion rate of jobs is <{completion_rate_jobs}>.
The eariliest time of this order over time step is <{eariliest_time}>.
The processing time of this job on me is <{part_need_time}>."""
        return prompt
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
        self.part_template = part_template
        [self.pre_buffer.addPart(part) for part in deepcopy(self.part_template)]

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
        # Always take the first part in the buffer.
        return self.pre_buffer.takePart(0)

    def onTickTickSecond(self, new_time: int):
        """
        Warehouse need not be called.
        @override
        :param new_time: int
        :return:
        """
        pass

    def reset(self):
        self.pre_buffer.reset()
        [self.pre_buffer.addPart(part) for part in deepcopy(self.part_template)]
