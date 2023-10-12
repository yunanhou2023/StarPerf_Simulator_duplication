'''

作者 ： 侯玉南

日期 ： 2023年8月24日18:47:22

功能 ： 实现星座中卫星间ISL以+Grid连接

函数输入 ： 没有任何ISL的卫星星座(即每一个卫星都是一个节点，节点之间没有任何边)

函数返回 ： 已经按照+Grid模式建立好连接的卫星星座(即每一个卫星都有4条ISL与同轨道前后两个卫星及相邻轨道两颗卫星建立连接)


该文件执行完后，传入的constellation中各个shell内的卫星之间已建立好ISL，并且也将各个卫星之间的延迟时间矩阵写到了Constellation_Snapshot文件夹下
'''
import os
from math import radians, cos, sin, asin, sqrt

import numpy as np

import Constellation_Entity.ISL as ISL_module

# 将某一时刻某一层shell的星座的延迟矩阵保存到文件中
def save_delay_to_file(delay, file_name):
    lines = []
    with open(file_name, 'w') as f:
        for d in delay:
            # 使用 join 数将 temp 和 element_Label以制表符为分隔符连接到一起
            line = '\t'.join([(str(x) if type(x) == int else str(x)[1:-1]) for x in d])
            # 将字符串添加到字符串列表中
            lines.append(line)
        result = '\n'.join(lines)
        f.writelines(result)
    f.close()

# 按照卫星的id查找对应的卫星，传入的参数sh是卫星星座的某一层shell，target_id是待查找的卫星的id号码
def search_satellite_by_id(sh , target_id):
    number_of_satellites_in_sh = sh.number_of_satellites  # sh层shell包含的卫星总数
    number_of_orbits_in_sh = sh.number_of_orbits  # sh层shell包含的轨道总数
    number_of_satellites_per_orbit = (int)(number_of_satellites_in_sh / number_of_orbits_in_sh)  # sh层shell中，每个轨道包含的卫星数
    # 按照卫星的id查找对应的卫星
    for orbit_index in range(1, number_of_orbits_in_sh + 1, 1):  # 逐层遍历每个轨道，orbit_index从1开始
        for satellite_index in range(1, number_of_satellites_per_orbit + 1, 1):  # 遍历每个轨道内的卫星，satellite_index从1开始
            satellite = sh.orbits[orbit_index - 1].satellites[satellite_index - 1]  # 获取卫星对象
            if satellite.id == target_id :
                return satellite


# 计算两颗卫星之间的距离（计算结果考虑了地球的曲率），返回值的单位是千米
def distance_two_satellites(satellite1 , satellite2):
    longitude1 = satellite1.longitude
    latitude1 = satellite1.latitude
    longitude2 = satellite2.longitude
    latitude2 = satellite2.latitude
    altitude = 1.0 * (satellite1.altitude + satellite2.altitude) / 2  # 高度以两个卫星的平均海拔高度作为高度，单位是千米
    longitude1,latitude1,longitude2,latitude2 = map(radians, [float(longitude1), float(latitude1), float(longitude2), float(latitude2)]) # 经纬度转换成弧度
    dlon=longitude2-longitude1
    dlat=latitude2-latitude1
    a=sin(dlat/2)**2 + cos(latitude1) * cos(latitude2) * sin(dlon/2)**2
    distance=2*asin(sqrt(a))*(6371.0+altitude)*1000 # 地球平均半径6371km，卫星轨道高度altitude（千米）
    distance=np.round(distance/1000,3)  # 将结果转化为千米为单位，保留三位小数
    return distance



# 传入参数含义 ： constellation是要建立+Grid连接的星座，t表示某一个时隙（timeslot）
def positive_Grid(constellation , t):
    # 逐层处理星座，分别处理每一个shell
    for sh_index,sh in enumerate(constellation.shells): #sh是constellation.shells中存储的shell对象，sh_index是sh在constellation.shells中的下标
        number_of_satellites_in_sh = sh.number_of_satellites  # sh层shell包含的卫星总数
        number_of_orbits_in_sh = sh.number_of_orbits  # sh层shell包含的轨道总数
        number_of_satellites_per_orbit = (int)(number_of_satellites_in_sh / number_of_orbits_in_sh)  # sh层shell中，每个轨道包含的卫星数

        # 建立卫星之间点的距离矩阵，存放任意两颗卫星之间的距离，单位是千米km,这里计算两颗卫星之间的距离使用的不是直线距离，而是考虑了地球曲率的距离，下标为0的行和列空着不用，从第1行第1列开始存放数据
        distance = [[0 for j in range(number_of_satellites_in_sh+1)] for i in range(number_of_satellites_in_sh+1)]
        # 建立卫星之间点的延迟矩阵，存放任意两颗卫星之间的延迟时间，单位是秒s，下标为0的行和列空着不用，从第1行第1列开始存放数据
        delay = [[0 for j in range(number_of_satellites_in_sh+1)] for i in range(number_of_satellites_in_sh+1)]

        # 计算一个卫星到其他卫星的距离和延迟
        for orbit_index in range(1,number_of_orbits_in_sh+1 , 1):  #逐层遍历每个轨道，orbit_index从1开始
            for satellite_index in range(1 , number_of_satellites_per_orbit+1 , 1): #遍历每个轨道内的卫星，satellite_index从1开始
                cur_satellite = sh.orbits[orbit_index - 1].satellites[satellite_index - 1]  # 获取当前卫星对象
                cur_satellite_id = cur_satellite.id # 获取当前卫星的id号
                # 获取当前卫星的前面一个卫星的id
                if satellite_index != number_of_satellites_per_orbit:
                    up_satellite_id = cur_satellite_id+1
                else:
                    up_satellite_id = cur_satellite_id+1-satellite_index
                # 根据id号up_satellite_id找到对应的卫星对象up_satellite
                up_satellite = search_satellite_by_id(sh , up_satellite_id)
                # 计算两颗卫星之间的距离
                distance[cur_satellite_id][up_satellite_id] = distance_two_satellites(cur_satellite , up_satellite)
                distance[up_satellite_id][cur_satellite_id] = distance[cur_satellite_id][up_satellite_id]
                # 计算两颗卫星之间的延迟
                delay[cur_satellite_id][up_satellite_id] = 1.0 * distance[cur_satellite_id][up_satellite_id] / 300000.0
                delay[up_satellite_id][cur_satellite_id] = delay[cur_satellite_id][up_satellite_id]
                # 建立相应的ISL对象
                isl = ISL_module.ISL(cur_satellite, up_satellite, distance[cur_satellite_id][up_satellite_id] ,
                                     delay[cur_satellite_id][up_satellite_id])
                # 在当前卫星中添加ISL对象表示已建立一个ISL连接
                cur_satellite.ISL.append(isl)
                # 在up_satellite卫星中添加ISL对象表示已建立一个ISL连接
                up_satellite.ISL.append(isl)

                # 获取当前卫星的右侧卫星的id
                if orbit_index != number_of_orbits_in_sh:
                    right_satellite_id = orbit_index * number_of_satellites_per_orbit + satellite_index
                else:
                    if sh.inclination > 80 and sh.inclination < 100:
                        continue
                    else:
                        right_satellite_id = satellite_index
                # 根据id号right_satellite_id找到对应的卫星对象right_satellite
                right_satellite = search_satellite_by_id(sh, right_satellite_id)
                # 计算两颗卫星之间的距离
                distance[cur_satellite_id][right_satellite_id] = distance_two_satellites(cur_satellite, right_satellite)
                distance[right_satellite_id][cur_satellite_id] = distance[cur_satellite_id][right_satellite_id]
                # 计算两颗卫星之间的延迟
                delay[cur_satellite_id][right_satellite_id] = 1.0 * distance[cur_satellite_id][right_satellite_id] / 300000.0
                delay[right_satellite_id][cur_satellite_id] = delay[cur_satellite_id][right_satellite_id]
                # 建立相应的ISL对象
                isl = ISL_module.ISL(cur_satellite, right_satellite, distance[cur_satellite_id][right_satellite_id],
                                     delay[cur_satellite_id][right_satellite_id])
                # 在当前卫星中添加ISL对象表示已建立一个ISL连接
                cur_satellite.ISL.append(isl)
                # 在up_satellite卫星中添加ISL对象表示已建立一个ISL连接
                right_satellite.ISL.append(isl)

        # 将该层shell（sh）在该时刻t的距离矩阵、延迟矩阵、星座各个卫星的位置保存到文件
        # 定义延迟矩阵写入的文件路径和文件名称
        delay_file_path_and_name = "Constellation_Connection/Constellation_Snapshot/" + \
                                   constellation.constellation_name + "/delay/shell_" + str(sh_index+1) + "/timeslot_"+ str(t) + ".txt"
        # 创建目录（如果不存在）
        os.makedirs(os.path.dirname(delay_file_path_and_name), exist_ok=True)
        # 将延迟矩阵delay写入文件，这里只需要写入delay矩阵即可，不需要保存distance矩阵，也不需要保存各个卫星的位置
        save_delay_to_file(delay , delay_file_path_and_name)
