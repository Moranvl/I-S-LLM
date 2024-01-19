from intelligent_shopfloor_environment.shopfloor import ShopFloor, ShopfloorLLM
from intelligent_shopfloor_environment.utils import analysisDataFile

if __name__ == '__main__':
    # print( analysisDataFile("./dataset/FJSSPinstances/1_Brandimarte/BrandimarteMk1.fjs") )
    sf = ShopfloorLLM("./dataset/FJSSPinstances/1_Brandimarte/BrandimarteMk1.fjs")
    sf.run()
    sf.reset()
    sf.run()
    data = sf.over_parts.printData()
    machine_processing = [list() for _ in range(6)]
    for part_processing_data in data:
        for i, machine_index in enumerate(part_processing_data[0]):
            machine_processing[machine_index-1].append(
                (part_processing_data[1][i], part_processing_data[2][i])
            )
    print(machine_processing)
    sf.plotData()
    # [len(m.pre_buffer.buffer_list) for m in sf.machines]
