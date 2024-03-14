from intelligent_shopfloor_environment.llm_shopfloor import ShopfloorLLM
from intelligent_shopfloor_environment.utils import analysisDataFile
from main import print_sf_and_plot_gantt

if __name__ == '__main__':
    # print( analysisDataFile("./dataset/FJSSPinstances/1_Brandimarte/BrandimarteMk1.fjs") )
    sf = ShopfloorLLM("./dataset/FJSSPinstances/1_Brandimarte/BrandimarteMk12.fjs")
    sf.run()
    print_sf_and_plot_gantt(sf)
    # sf.reset()
    # sf.run()
    # # sf.reset()
    # # sf.run()
