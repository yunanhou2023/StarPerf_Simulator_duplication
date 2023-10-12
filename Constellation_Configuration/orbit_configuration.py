'''

作者 ： 侯玉南

日期 ： 2023年8月26日09:47:12

功能 ： 该文件定义了生成轨道的函数。函数的传入参数是一个shell对象sh，无返回值

'''
import Constellation_Entity.orbit as Orbit
import Constellation_Entity.satellite as Satellite
import math
import skyfield
from skyfield.api import load, wgs84, EarthSatellite
from datetime import datetime, date, time, timezone,timedelta
import time
from sgp4.api import Satrec, WGS72
import numpy as np
import pandas as pd


def orbit_configuration(sh):
    a = 6371.0 + sh.altitude # 卫星轨道半长轴,单位：千米
    inc = sh.inclination # 轨道倾角，单位是°
    ecc = 0  # 设置轨道偏心率
    argp = 0  # 设置轨道近地点幅角，当偏心率ecc=0时，轨道为标准圆形，近地点与升交点重合，此时近地点幅角为0
    raan = []  # 生成卫星轨道的升交点赤经，sh层shell有多少个轨道，raan的长度就是多长
    if inc > 80 and inc < 100:
        raan = [i * (180.0/sh.number_of_orbits) for i in range(sh.number_of_orbits)]
    else:
        raan = [i * (360.0/sh.number_of_orbits) for i in range(sh.number_of_orbits)]
    # 生成同一轨道内相邻两颗卫星之间的夹角
    meanAnomaly1 = [i * (360.0/sh.number_of_satellite_per_orbit) for i in range(sh.number_of_satellite_per_orbit)]
    ts = load.timescale()
    since = datetime(1949, 12, 31, 0, 0, 0)
    start = datetime(2023, 10, 1, 0, 0, 0)
    epoch = (start - since).days  # epoch表示since和start两个日期之间的天数
    inc = inc * 2 * np.pi / 360  # 轨道倾角（弧度制）
    GM = 3.9860044e14  # 地球的引力常数，等于地球质量乘以万有引力常数
    R = 6371393  # 地球半径（米）
    altitude = sh.altitude * 1000  # 轨道高度（米）
    mean_motion = np.sqrt(GM / (R + altitude) ** 3) * 60  # 卫星的平均运行速度
    num_of_orbit = sh.number_of_orbits  # 轨道数量
    sat_per_orbit = sh.number_of_satellite_per_orbit  # 每轨卫星数量
    num_of_sat = num_of_orbit * sat_per_orbit  # 总卫星数量
    F = 1
    for i in range(1 , sh.number_of_orbits+1, 1):
        orbit = Orbit.orbit(a=a , ecc=ecc , inc=inc , raan=raan[i-1] , argp = argp)
        for j in range(1 , sh.number_of_satellite_per_orbit+1 , 1):
            # 在这里生成每一颗卫星…… 生成卫星后将每一颗卫星加入orbit对象的satellites属性中
            nu = meanAnomaly1[j-1]  # 卫星的真近点角
            satrec = Satrec()
            satrec.sgp4init(
                WGS72,  # 坐标系
                'i',  # 'a' = old AFSPC mode, 'i' = improved mode
                i * sat_per_orbit + j,  # satnum: Satellite number 卫星编号
                epoch,  # epoch: days since 1949 December 31 00:00 UT 日期
                2.8098e-05,  # bstar: drag coefficient (/earth radii) 阻力系数
                6.969196665e-13,  # ndot: ballistic coefficient (revs/day) 弹道系数
                0.0,  # nddot: second derivative of mean motion (revs/day^3) 平均运动的二阶导数
                0.0,  # ecco: eccentricity 偏心率
                0.0,  # argpo: argument of perigee (radians) 近地点幅角
                inc,  # inclo: inclination (radians) 轨道倾角
                math.radians(nu),  # mo: mean anomaly (radians) 平均近点角
                mean_motion,  # no_kozai: mean motion (radians/minute) 平均运动
                math.radians(raan[i-1]),  # nodeo: right ascension of ascending node (radians) 升交点赤经
            )
            sat = EarthSatellite.from_satrec(satrec, ts)  # 生成卫星对象
            t_ts = ts.utc(2023, 10, 1, 0, range(1))  # 创建了一个包含1分钟内时间戳的列表，共1个元素
            geocentric = sat.at(t_ts)
            subpoint = wgs84.subpoint(geocentric)
            latitude = subpoint.latitude.degrees
            longitude = subpoint.longitude.degrees
            altitude = subpoint.elevation.km
            satellite = Satellite.satellite(nu=nu , orbit=orbit , latitude=latitude ,
                                            longitude=longitude , altitude=altitude , true_satellite = sat)
            orbit.satellites.append(satellite)
        sh.orbits.append(orbit)