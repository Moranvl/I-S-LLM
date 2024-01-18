"""
Define the parts and part buffer.
"""
import matplotlib.pyplot as plt
from intelligent_shopfloor_environment.utils import plot_gantt_one_part


class Part:
    """The part to be processed"""

    def __init__(self, index, process_tuple: tuple[dict], due_time: int = 0):
        """
            - processes_tuple: ({machine1:time1, machine2:time2}, ... ,{machine1:time1, machine2:time2})
        """
        self.index = index
        self.processes_tuple = process_tuple
        self.processes_len = len(process_tuple) - 1
        # the processes index which is over
        self.processes_index: int = -1
        self.due_time: int = due_time
        # processing data
        self.processing_data = (list(), list(), list())

    def isOver(self) -> bool:
        """check if the part is over"""
        return self.processes_index > self.processes_len

    def process(self) -> None:
        """Operate the part."""
        self.processes_index += 1

    def getProcessingTime(self, machine_index: int) -> int:
        """get the processing time of the part"""
        return self.processes_tuple[self.processes_index][machine_index]

    def getNowTimeDict(self) -> dict:
        """get the time dictionary now"""
        return self.processes_tuple[self.processes_index]

    # region save processing data
    def saveMachineID(self, machine_id: int):
        self.processing_data[0].append(machine_id)

    def saveStartTime(self, start_time: int):
        self.processing_data[1].append(start_time)

    def saveEndTime(self, end_time: int):
        self.processing_data[2].append(end_time)
    # endregion


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

    def printData(self):
        for part in self.buffer_list:
            print(part.processing_data)
        return [part.processing_data for part in self.buffer_list]

    def plotData(self, machine_num: int):
        """plot gantt figure for shopfloor"""
        # 初始化图形和坐标轴范围
        plt.figure(figsize=(20, 5))
        # 设置y轴标签和范围
        plt.yticks(range(machine_num), list(range(1, machine_num + 1)))
        plt.xlabel('Time Steps')
        plt.ylabel('Machine Numbers')
        # 添加额外的样式设置
        plt.title('Gantt Chart')
        # plt.grid(axis='x')

        max_time_list = list()
        for part in self.buffer_list:
            max_time = plot_gantt_one_part(
                part.processing_data[0], part.processing_data[1], part.processing_data[2],
                part_index=part.index+1, color="skyblue"
            )
            max_time_list.append(max_time)
        plt.xlim(0, max(max_time_list))
        plt.show()
