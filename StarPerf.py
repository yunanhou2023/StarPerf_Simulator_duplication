'''
改造后的StarPerf

Python版本 ： Python3.10
'''

import Constellation_Configuration.constellation_configuration as constellation_configuration
import Constellation_Connection.connection_mode_plugin_manager as connection_mode_plugin_manager
import Constellation_Evaluation.delay as DELAY
import Constellation_Entity.ground_station as GS

source = GS.ground_station("London" , 0.00 , 51.30) # 源地面站
target = GS.ground_station("NewYork" , -74.00 , 40.43) # 目标地面站
constellation=constellation_configuration.constellation_configuration() # 生成星座
connectionModePluginManager = connection_mode_plugin_manager.connection_mode_plugin_manager() # 初始化连接模式插件管理器
print(connectionModePluginManager.current_connection_mode) # 打印当前所使用的连接模式
connectionModePluginManager.execute_connection_policy(constellation=constellation , t=0) # 在星座中建立ISL连接
delay = DELAY.delay("StarLink" , "shell_5" , source , target , 0 , constellation.shells[4]) # 计算延迟
print("从" , source.station_name  , "到" , target.station_name , "的延迟是" , delay*1000 , "ms")








'''
constellation=constellation_configuration.constellation_configuration()
shell1 = constellation.shells[0]

for i in range(shell1.number_of_orbits):
    for j in range(len(shell1.orbits[i].satellites)):
        print("i = " , i , " , j = " , j , " , longitude = " , shell1.orbits[i].satellites[j].longitude ,
              " , latitude = " , shell1.orbits[i].satellites[j].latitude , " , altitude = " ,
              shell1.orbits[i].satellites[j].altitude)
'''





'''
count=1
for sh in constellation.shells:
    for orb in sh.orbits:
        for sat in orb.satellites:
            print("sat.orbit.a = " , sat.orbit.a)
            print("sat.orbit.ecc = " , sat.orbit.ecc)
            print("sat.orbit.inc = " , sat.orbit.inc)
            print("sat.orbit.raan = " , sat.orbit.raan)
            print("sat.orbit.argp = " , sat.orbit.argp)
            print("sat.orbit.orbit_cycle = " , sat.orbit.orbit_cycle)
            print("sat.nu = " , sat.nu)
            print("count=" , count)
            count = count+1
'''


