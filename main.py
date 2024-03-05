from intelligent_shopfloor_environment.shopfloor import ShopFloor
from intelligent_shopfloor_environment.utils import analysisDataFile


def print_sf_and_plot_gantt(shopfloor: ShopFloor):
    data = sf.over_parts.printData()
    machine_processing = [list() for _ in range(6)]
    for part_processing_data in data:
        for i, machine_index in enumerate(part_processing_data[0]):
            machine_processing[machine_index - 1].append(
                (part_processing_data[1][i], part_processing_data[2][i])
            )
    print(machine_processing)
    sf.plotData()
    # [len(m.pre_buffer.buffer_list) for m in sf.machines]


if __name__ == '__main__':
    # print( analysisDataFile("./dataset/FJSSPinstances/1_Brandimarte/BrandimarteMk1.fjs") )
    sf = ShopFloor("./dataset/FJSSPinstances/1_Brandimarte/BrandimarteMk1.fjs")
    sf.run()
    # print_sf_and_plot_gantt(sf)
    # sf.reset()
    # sf.run()
    # # sf.reset()
    # # sf.run()
