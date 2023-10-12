'''

作者 ： 侯玉南

日期 ： 2023年8月24日11:40:13

功能 ： 该文件定义了星间链路类ISL，是本项目中所有ISL的基类
       ISL负责连接两颗卫星，不具有方向性，因此无需区分源卫星和目的卫星

？ ？ ？  这里目前存在的疑问：要描述一个ISL，需要使用哪些字段？需要包含哪些方法？这里目前只定义了源卫星、目的卫星、数据速率、频段及容量，还有其他必要的字段吗？

'''


class ISL:
    def __init__(self , satellite1 , satellite2 ,distance , delay ,data_rate=100, frequency_band =100, capacity =100):
        self.satellite1 = satellite1 #第一卫星
        self.satellite2 = satellite2 #第二卫星
        self.distance = distance  # ISL所连接的两颗卫星之间的距离，单位是千米km
        self.delay = delay  # ISL所连接的两颗卫星之间的延迟，单位是秒s
        self.data_rate = data_rate  #数据传输速率(bps)
        self.frequency_band = frequency_band #激光频段
        self.capacity = capacity #ISL容量


