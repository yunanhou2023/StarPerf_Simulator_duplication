'''

作者 ： 侯玉南

日期 ： 2023年8月24日12:01:08

功能 ： 该文件定义了卫星类satellite，是本项目中所有卫星的基类
       确定卫星在轨道上的位置需要经度、纬度、距离地球表面的距离、真近点角等参数

'''

class satellite:
    def __init__(self , nu , orbit , longitude , latitude , altitude , true_satellite):
        self.longitude = longitude #经度（角度）
        self.latitude = latitude #纬度（角度）
        self.altitude = altitude #高度（千米）
        #self.TLE = TLE #卫星的TLE数据
        self.orbit = orbit # 表示当前卫星所在的轨道的轨道对象
        self.ISL = [] #list类型属性，存放当前卫星与哪些卫星建立了ISL，存放的是ISL对象
        self.nu = nu  # 真近点角，描述物体在轨道上的位置的参数，它表示了物体在轨道上的位置相对于近地点的角度。对于不同的时间，真近点角的值会不断变化，因为物体在轨道上移动。
        # 卫星的id号，该id号是卫星在其所在的shell内的编号。如果星座有多个shell，则每个卫星的id都是其所在shell的编号。每层shell均从1开始编号
        # id号初始为-1，用户无需手动指定
        self.id = -1
        self.true_satellite = true_satellite # 真正的卫星对象，该对象由sgp4和skyfield模型创建
