"""
Define the parts and part buffer.
"""
import matplotlib
import matplotlib.pyplot as plt
from intelligent_shopfloor_environment.utils import (
    plot_gantt_one_part, generate_distinct_colors, calculate_middle_value_in_gantt
)


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

    def getSumProcessingTime(self, this_machine_index) -> int:
        sum_time = 0
        for part in self.buffer_list:
            sum_time += part.getProcessingTime(this_machine_index)
        return sum_time

    def getProcessingTimeList(self, this_machine_index) -> list:
        return [p.getProcessingTime(this_machine_index) for p in self.buffer_list]
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

    def plotData(
            self, machine_num: int, end_time: int, figsize=(6.6929134, 4), save_dir=None, plot_adjust=None,
            need_text=True
    ):
        """plot gantt figure for shopfloor"""
        matplotlib.rcParams.update({'font.size': 16})

        # 一些计算
        x_end = end_time % 5
        x_end = 5 - x_end + end_time
        calcute_mid_value = calculate_middle_value_in_gantt(x_end)
        x_ticks = list(range(0, end_time, calcute_mid_value))
        if x_ticks[-1] != end_time:
            if end_time - x_ticks[-1] < calcute_mid_value * 0.3:
                x_ticks[-1] = end_time
            else:
                x_ticks.append(end_time)

        # 初始化图形和坐标轴范围
        plt.figure(figsize=figsize, dpi=300)
        # 调整网格
        if plot_adjust is not None:
            plt.subplots_adjust(top=plot_adjust[0], bottom=plot_adjust[1], left=plot_adjust[2], right=plot_adjust[3])
        # 调整网格线
        ax = plt.gca()
        for a in ["left", "top", "right", "bottom"]:
            ax.spines[a].set_linewidth(1.5)
        # ax.spines["right"].set_visible(False)
        # ax.spines["top"].set_visible(False)
        plt.grid(axis="x", zorder=-100)
        # 设置y轴标签和范围
        plt.yticks(range(machine_num), [f"M{index}" for index in list(range(1, machine_num + 1))])
        plt.xticks(x_ticks, x_ticks)
        plt.xlim(0, x_end)
        plt.ylim(-1, machine_num)

        plt.xlabel('Time Steps')
        plt.ylabel('Machines')
        # 添加额外的样式设置
        plt.title('Gantt Chart')
        # plt.grid(axis='x')

        max_time_list = list()
        distinct_colors_hex = generate_distinct_colors(len(self.buffer_list))
        for i, part in enumerate(self.buffer_list):
            max_time = plot_gantt_one_part(
                part.processing_data[0], part.processing_data[1], part.processing_data[2],
                part_index=part.index + 1, color=distinct_colors_hex[i], need_text=need_text
            )
            max_time_list.append(max_time)
        # plt.xlim(0, max(max_time_list))
        # 在结束的地方画一条竖线
        plt.axvline(x=end_time, color="red", linestyle="--", zorder=150, linewidth=1)
        if save_dir is not None:
            plt.savefig(save_dir, dpi=1200)
        plt.show()
