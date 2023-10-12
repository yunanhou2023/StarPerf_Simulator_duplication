'''

作者 ： 侯玉南

日期 ： 2023年8月24日13:14:11

功能 ： 该文件定义了星座类，包括星座名称，星座的一些参数（如有几层shell，一共有多少卫星，一共有多少轨道等）
       该类也是单例模式类，全局只能有一个星座
'''

# 定义单例模式点的装饰器
def __singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance

@__singleton
class constellation:
    def __init__(self , constellation_name , number_of_shells , shells):
        self.constellation_name = constellation_name  # 星座名称
        self.number_of_shells = number_of_shells  # 星座包含的shell数量
        self.shells = shells  # 星座包含哪些shell，是list类型，存放的是shell类对象