'''

作者 ： 侯玉南

日期 ： 2023年8月24日12:51:42

功能 ： 该文件定义了轨道类，用于描述一个卫星轨道的相关参数，这里考虑椭圆形，唯一确定出一个轨道需要5个参数：轨道半长轴、轨道倾角、升交点赤经、偏心率、近地点幅角
'''
import math
from poliastro.bodies import Earth
from poliastro.twobody import Orbit
from astropy import units as u



class orbit:
    def __init__(self , a , ecc , inc , raan , argp):
        self.a = a * u.km #轨道半长轴，单位是千米km
        self.ecc = ecc * u.one #轨道偏心率
        self.inc = inc * u.deg # 轨道的倾角，单位是度°
        self.raan = raan * u.deg # 轨道升交点赤经
        self.argp = argp * u.deg # 近地点幅角，单位是角度
        self.orbit_cycle = 2 * math.pi * math.sqrt((a*1000) ** 3 / (6.67430e-11 * 5.972e24))  # 计算轨道周期（单位：秒）
        # 实际卫星轨道
        self.satellite_orbit = Orbit.from_classical(
            Earth,
            a=self.a,
            ecc=self.ecc,
            inc=self.inc,
            raan=self.raan,
            argp=self.argp,
            nu=0 * u.deg  # 真近点角，是用来描述卫星的，这里是生成轨道，该参数不起作用，仅占位
        )
        self.satellites = [] #list类型字段，用来存放该轨道内的卫星，存放的是卫星对象

