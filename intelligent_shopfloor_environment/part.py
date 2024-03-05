"""
Define the parts and part buffer.
"""
import matplotlib.pyplot as plt
from intelligent_shopfloor_environment.utils import plot_gantt_one_part, generate_distinct_colors


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

    # region Get Information
    def getProcessingTime(self, machine_index: int) -> int:
        """get the processing time of the part"""
        return self.processes_tuple[self.processes_index][machine_index]

    def getNowTimeDict(self) -> dict:
        """get the time dictionary now"""
        return self.processes_tuple[self.processes_index]

    def getProcessingMachineList(self) -> list[int]:
        return [machine_id for machine_id in self.processes_tuple[self.processes_index]]

    def getNowStartTime(self) -> int:
        return self.processes_tuple[1][-1]

    def getOperationIndex(self) -> tuple[int, ...]:
        return self.processes_index, self.processes_len
    # endregion

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

    def reset(self):
        self.buffer_list.clear()

    # region Get Information
    def getLength(self) -> int:
        return len(self.buffer_list)

    def getCompletionRate(self) -> tuple[float, ...]:
        """Get the completion rate of operations and jobs"""
        sum_operation = 0
        sum_all_operations = 0
        len_buffer = self.getLength()
        completion_rate_jobs = 0.

        completion_rate_operations = 0
        completion_rate_jobs = 0
        if len(self.buffer_list) != 0:
            for part in self.buffer_list:
                operation_num, all_operations_num = part.getOperationIndex()
                sum_operation += operation_num
                sum_all_operations += all_operations_num
                completion_rate_jobs += operation_num / all_operations_num
            completion_rate_operations = sum_operation / sum_all_operations
            completion_rate_jobs /= len_buffer
        return completion_rate_operations, completion_rate_jobs
    # endregion


class OverPartBuffer:
    """Sotre the over parts."""

    def __init__(self):
        self.buffer_list: list[Part] = list()
        self.buffer_list_append = self.buffer_list.append

    def addPart(self, part: Part) -> None:
        """Add a part to the buffer"""
        self.buffer_list_append(part)

    def reset(self) -> None:
        self.buffer_list.clear()

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
        distinct_colors_hex = generate_distinct_colors(len(self.buffer_list))
        for i, part in enumerate(self.buffer_list):
            max_time = plot_gantt_one_part(
                part.processing_data[0], part.processing_data[1], part.processing_data[2],
                part_index=part.index + 1, color=distinct_colors_hex[i]
            )
            max_time_list.append(max_time)
        plt.xlim(0, max(max_time_list))
        plt.show()
