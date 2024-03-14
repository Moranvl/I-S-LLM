from intelligent_shopfloor_environment.shopfloor import ShopFloor
from intelligent_shopfloor_environment.utils import analysisDataFile


def print_sf_and_plot_gantt(shopfloor: ShopFloor):
    data = shopfloor.over_parts.printData()
    machine_processing = [list() for _ in range(shopfloor.getMachineNum())]
    for part_processing_data in data:
        for i, machine_index in enumerate(part_processing_data[0]):
            machine_processing[machine_index - 1].append(
                (part_processing_data[1][i], part_processing_data[2][i])
            )
    print(machine_processing)
    shopfloor.plotData(figsize=(17, 8), save_dir=None)
    # [len(m.pre_buffer.buffer_list) for m in sf.machines]


if __name__ == '__main__':
    # print( analysisDataFile("./dataset/FJSSPinstances/1_Brandimarte/BrandimarteMk1.fjs") )
    figsize_list = [
        (17, 8), (17, 8), (17, 8), (17, 8), (17, 5.5),
        (17, 8), (17, 6), (17, 8), (17, 8), (17, 8),
        (17, 6), (17, 8), (17, 8), (17, 8), (17, 8),
    ]
    # sf = ShopFloor(f"./dataset/FJSSPinstances/1_Brandimarte/BrandimarteMk14.fjs")
    # sf.run()
    # sf.plotData(figsize=(17, 8), save_dir=None, plot_adjust=[0.9, 0.1, 0.05, 0.95])
    for i in range(1, 16):
        sf = ShopFloor(f"./dataset/FJSSPinstances/1_Brandimarte/BrandimarteMk{i}.fjs")
        sf.run()
        sf.plotData(figsize=figsize_list[i-1], save_dir=f"./results/test/mk{i}.tiff", plot_adjust=[0.9, 0.1, 0.05, 0.95])

    # print_sf_and_plot_gantt(sf)
    # sf.reset()
    # sf.run()
    # # sf.reset()
    # # sf.run()
