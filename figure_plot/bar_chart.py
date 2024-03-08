import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import math
def plot_multi_bar_chart(
        input_x, input_y: list, y_labels: list,
        color_map=None, bar_width=0.4, save_filename=None, fig_size=(3.2677165, 2),
        x_label="Cities", y_label="Population (in thousands)", title="City Population by Gender"
):
    matplotlib.rcParams.update({'font.size': 8})

    length = len(input_y)
    index = np.arange(len(input_x)) * (math.ceil(length * bar_width))

    # 3.2677165, 6.9291339 (8.3, 17.6) （80 110 180）
    plt.figure(figsize=fig_size, dpi=300)
    for i, content in enumerate(input_y):
        plt.bar(
            index + i * bar_width, input_y[i], bar_width, label=y_labels[i], color=color_map[i],
        )
    plt.xticks(index + bar_width * (length - 1) / 2, input_x)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend(loc='best')
    plt.show()

    if save_filename is not None:
        plt.savefig(save_filename, dpi=1200)


if __name__ == '__main__':
    # 同样的数据集
    cities = ['Beijing', 'Shanghai', 'Tianjin', 'Chongqing']
    male_population = [1000, 1200, 800, 1500]
    female_population = [900, 1300, 750, 1400]
    data = [male_population, female_population]

    plot_multi_bar_chart(input_x=cities, input_y=data, y_labels=[1, 3], color_map=["#263f6d", "#972e32"])
