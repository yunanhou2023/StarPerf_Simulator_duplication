'''

作者 ： 侯玉南

日期 ： 2023年8月24日20:43:01

功能 ： 该文件定义了地面观测站类，通信中需要指定的源端点和目的端点，这些端点就是该类的实例化对象
       观测站都设在地球表面，实例化观测站时必须传入经纬度

'''

class ground_station:
    def __init__(self , station_name, longitude, latitude):
        self.station_name = station_name # 观测站名称
        self.longitude = longitude # 观测站经度
        self.latitude = latitude #观测站纬度