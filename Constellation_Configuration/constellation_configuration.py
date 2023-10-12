'''

作者 ： 侯玉南

日期 ： 2023年8月25日18:48:50

功能 ： 该文件定义了星座配置信息函数，包括星座名称、shell数量、卫星数量、轨道数量、倾角、轨道高度等，该函数的作用是读取constellation_configuration.properties配置文件的数据

'''
import Constellation_Configuration.Properties as Properties
import Constellation_Entity.shell as shell
import Constellation_Configuration.orbit_configuration as orbit_configuration
import Constellation_Entity.constellation as Constellation

def constellation_configuration():
    # 星座配置信息文件.properties文件的路径
    properties_file_path = "Constellation_Configuration/constellation_configuration.properties"
    # 声明一个Properties类的实例，调用其getProperties方法，返回一个字典
    constellation = Properties.Properties(properties_file_path).getProperties()
    # .properties文件的所有参数都存在字典的value中
    constellation_name = constellation['constellation_name']
    number_of_shells = int(constellation['number_of_shells']) # 字符串转成int类型
    shells = []
    for count in range(1 , number_of_shells+1 , 1):
        altitude = int(constellation['shell' + str(count) + '_altitude'])
        orbit_cycle = int(constellation['shell' + str(count) + '_orbit_cycle'])
        inclination = float(constellation['shell' + str(count) + '_inclination'])
        phase_shift = int(constellation['shell' + str(count) + '_phase_shift'])
        number_of_orbit = int(constellation['shell' + str(count) + '_number_of_orbit'])
        number_of_satellite_per_orbit = int(constellation['shell' + str(count) + '_number_of_satellite_per_orbit'])
        sh = shell.shell(altitude=altitude , number_of_satellites=number_of_orbit*number_of_satellite_per_orbit ,
                         number_of_orbits=number_of_orbit ,inclination=inclination , orbit_cycle=orbit_cycle ,
                         number_of_satellite_per_orbit=number_of_satellite_per_orbit , phase_shift=phase_shift)
        # sh层的基本属性已配置完毕，现在生成sh层的轨道
        orbit_configuration.orbit_configuration(sh)
        # sh层所有轨道和卫星都配置完毕，现在设置各个卫星的编号
        number_of_satellites_in_sh = sh.number_of_satellites  # sh层shell包含的卫星总数
        number_of_orbits_in_sh = sh.number_of_orbits  # sh层shell包含的轨道总数
        number_of_satellites_per_orbit = (int)(
            number_of_satellites_in_sh / number_of_orbits_in_sh)  # sh层shell中，每个轨道包含的卫星数
        # 给sh层内的每一个卫星编号，即修改卫星对象的id属性
        for orbit_index in range(1, number_of_orbits_in_sh + 1, 1):  # 逐层遍历每个轨道，orbit_index从1开始
            for satellite_index in range(1, number_of_satellites_per_orbit + 1, 1):  # 遍历每个轨道内的卫星，satellite_index从1开始
                satellite = sh.orbits[orbit_index - 1].satellites[satellite_index - 1]  # 获取卫星对象
                satellite.id = (orbit_index - 1) * number_of_satellites_per_orbit + satellite_index  # 设置当前卫星的id编号
        # 将当前shell层sh加入星座中
        shells.append(sh)

    # 所有shell、轨道、卫星均已初始化完毕，生成目标星座并返回
    target_constellation = Constellation.constellation(constellation_name=constellation_name,number_of_shells=number_of_shells ,
                                                      shells=shells)
    return target_constellation

