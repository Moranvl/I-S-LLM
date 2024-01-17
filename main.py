from intelligent_shopfloor_environment.shopfloor import ShopFloor, ShopfloorLLM
from intelligent_shopfloor_environment.utils import analysisDataFile

if __name__ == '__main__':
    # print( analysisDataFile("./dataset/FJSSPinstances/1_Brandimarte/BrandimarteMk1.fjs") )
    sf = ShopfloorLLM("./dataset/FJSSPinstances/1_Brandimarte/BrandimarteMk1.fjs")
    sf.run()
    # [len(m.pre_buffer.buffer_list) for m in sf.machines]
