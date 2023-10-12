'''

作者 ： 侯玉南

日期 ： 2023年8月24日13:01:34

功能 ： 该文件定义了星座的一层(即shell)，类中的字段描述了该shell的一些信息，包括shell的高度、包含的卫星数、包含的轨道数等

'''

class shell:
    def __init__(self , altitude , number_of_satellites , number_of_orbits , inclination , orbit_cycle ,
                 number_of_satellite_per_orbit , phase_shift):
        self.altitude = altitude #shell的高度(千米)
        self.number_of_satellites = number_of_satellites #本层shell包含的卫星数
        self.number_of_orbits = number_of_orbits  #本层shell包含的轨道数
        self.inclination = inclination # 本层shell的倾角
        self.orbit_cycle = orbit_cycle # 本层shell轨道周期
        self.number_of_satellite_per_orbit = number_of_satellite_per_orbit # 本层shell每轨卫星数
        self.phase_shift = phase_shift # 相移，用于生成卫星时使用
        self.orbits = [] #list类型对象，用来存放本层shell都包含了哪些轨道，存放的是orbit对象