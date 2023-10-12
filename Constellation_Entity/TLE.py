'''

作者 ： 侯玉南

日期 ： 2023年8月24日12:14:27

功能 ： 该文件定义了卫星的TLE数据类

'''

class TLE:
    def __init__(self , satellite_name , line1 , line2 , date):
        self.satellite_name=satellite_name #卫星名称
        self.line1=line1 #第一行TLE数据
        self.line2=line2 #第二行TLE数据
        self.date=date #TLE数据产生的日期