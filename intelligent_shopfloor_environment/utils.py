import matplotlib.pyplot as plt
from matplotlib.colors import rgb2hex
import numpy as np


# region Analysis the Files
def partStr2Dict(info: list[int]) -> tuple[dict, ...]:
    num_of_orders = info[0]
    part_template_list = list()

    processing_machine_num = 0
    order_list: list[dict] = list()
    index = 1
    temp_index = 0
    length_info = len(info)
    while index < length_info:
        processing_machine_num = info[index]

        order_list.append(dict())
        temp_index = index + 1
        while temp_index < index + processing_machine_num * 2 + 1:
            order_list[-1].update(
                {info[temp_index]: info[temp_index + 1]}
            )
            temp_index += 2
        index += processing_machine_num * 2 + 1
    return tuple(order_list)


def analysisDataFile(filename: str) -> tuple[int, list[tuple]]:
    """read the file and split file into lines"""
    with open(filename, "r") as file:
        lines = [line.rstrip('\n') for line in file.readlines() if line.strip()]
    # title = [num for num in lines[0].strip("\t")]
    title = [float(num) for num in lines[0].split()]
    content = [line.strip().split() for line in lines[1:]]
    content = [[int(num) for num in subcontent] for subcontent in content]
    assert len(content) == title[0]

    machine_num = title[1]
    partTupleList = [partStr2Dict(element) for element in content]
    assert len(partTupleList) == title[0]

    return int(machine_num), partTupleList


# endregion

# region Plot Gantt Figure
def plot_gantt_one_part(
        machine_id: list, start_steps: list, end_steps: list, part_index: int = 0, color: str = 'skyblue'
):
    """Plot gantt for one part. All parts must be plotted in one figure."""
    for order_index, (m_id, start, end) in enumerate(zip(machine_id, start_steps, end_steps)):
        plt.barh(m_id - 1, end - start, left=start, align='center', color=color, edgecolor="black", zorder=100)
        plt.text(
            start + (end - start) / 2, m_id - 1, f"{part_index},{order_index + 1}",
            ha="center", va='center', fontsize=8,
            zorder=101
            # fontweight="normal"
        )

    max_time = max(end_steps)
    return max_time


def generate_distinct_colors(n):
    """Get n colors"""
    cmap_name = 'tab20' if n <= 20 else 'rainbow'
    cmap = plt.colormaps[cmap_name]

    if isinstance(cmap, str):  # 如果'n > 20'且所选cmap是一个字符串（需要实例化）
        cmap = plt.colormaps.get_cmap(cmap, lut=n)  # 创建一个lut长度为n的新色彩映射表

    colors = [rgb2hex(cmap(i)[:3]) for i in np.linspace(0, 1, min(n, cmap.N))]
    return colors[:n]  # 返回前n种颜色


def calculate_middle_value_in_gantt(t):
    result = int(t / 10)
    if result < 5:
        result = 5
    elif result < 10:
        result = 10
    elif result < 20:
        result = 20
    elif result < 50:
        result = 50
    else:
        result =100

    return result
# endregion
