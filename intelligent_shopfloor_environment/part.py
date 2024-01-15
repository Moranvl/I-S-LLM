"""
Define the parts and part buffer.
"""


class Part:
    """The part to be processed"""

    def __init__(self, process_tuple: tuple[dict], due_time: int = 0):
        """
            - processes_tuple: ({machine1:time1, machine2:time2}, ... ,{machine1:time1, machine2:time2})
        """
        self.processes_tuple = process_tuple
        self.processes_len = len(process_tuple) - 1
        # the processes index which is over
        self.processes_index: int = -1
        self.due_time: int = due_time

    def isOver(self) -> bool:
        """check if the part is over"""
        return self.processes_index < self.processes_len

    def process(self) -> None:
        """Operate the part."""
        self.processes_index += 1

    def getProcessingTime(self, machine_index: int) -> int:
        """get the processing time of the part"""
        return self.processes_tuple[self.processes_index][machine_index]


class PartBuffer:
    """The part buffer to save parts."""

    def __init__(self):
        self.buffer_list: list[Part] = list()

    def addPart(self, part: Part) -> None:
        """Add a part to the buffer"""
        self.buffer_list.append(part)

    def takePart(self, index: int) -> Part:
        """take a part from the buffer"""
        temp_part = self.buffer_list.pop(index)
        return temp_part

    def isEmpty(self) -> bool:
        return len(self.buffer_list) == 0


class OverPartBuffer:
    """Sotre the over parts."""

    def __init__(self):
        self.buffer_list: list[Part] = list()
        self.buffer_list_append = self.buffer_list.append

    def addPart(self, part: Part) -> None:
        """Add a part to the buffer"""
        self.buffer_list_append(part)
