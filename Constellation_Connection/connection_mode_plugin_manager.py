'''

作者 ： 侯玉南

日期 ： 2023年8月24日15:26:32

功能 ： 该文件定义了关于星座中卫星间连接方式的管理器类，这是一个开放性接口，可以很容易地接入任何连接方式，比如motif、+Grid等
       该类采用单例模式，整个项目中从始至终只允许有一个管理器出现
       后续如果想加入新的连接模式，只需要按照接口规范文档编写函数就可以了
       要求 ： Connection_Plugin文件夹下存放的均为本项目所有的连接模式，每个py文件包含一个函数，一个函数就是一个连接模式的定义，函数名与文件名相同
'''

import importlib
import os

# 定义单例模式的装饰器
def __singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@__singleton
class connection_mode_plugin_manager:
    def __init__(self):
        self.plugins = {}  # 连接模式插件字典，存放本项目中所有的连接模式插件，字典的key是连接模式的函数名称，value是连接模式对应的函数
        # 下面的代码块用来遍历Connection_Plugin文件夹，该文件夹存放的是所有连接模式的py文件
        # 遍历这个文件夹获取所有的连接模式插件的名称，存放到self.plugins集合中
        package_name = "Constellation_Connection.Connection_Plugin"
        plugins_path = package_name.replace(".", os.path.sep) # 插件存放的路径
        for plugin_name in os.listdir(plugins_path):
            if plugin_name.endswith(".py"):
                plugin_name = plugin_name[:-3]  # 去掉文件扩展名.py
                plugin = importlib.import_module(package_name + "." + plugin_name)
                if hasattr(plugin, plugin_name) and callable(getattr(plugin, plugin_name)):
                    function = getattr(plugin, plugin_name)
                    self.plugins[plugin_name] = function
        self.current_connection_mode = "positive_Grid"  # 设置当前连接模式插件管理器使用的连接模式，默认采用+Grid方式连接

    # 该函数的作用是清空传入的卫星星座constellation中的所有ISL
    def clear_ISL(self , constellation):
        for shell in constellation.shells:
            for orbit in shell.orbits:
                for satellite in orbit.satellites:
                    satellite.ISL.clear()  #清空卫星的ISL


    # 切换连接模式，参数含义 ： plugin_name是新连接模式的名称，constellation是目标星座
    def set_connection_mode(self , plugin_name):
        self.current_connection_mode = plugin_name # 将当前连接模式设置为指定模式
        print("当前星座连接模式已切换为 " + plugin_name)


    #  执行星座连接模式，在星座中建立ISL
    def execute_connection_policy(self , constellation , t): # 传入的参数t是时隙
        self.clear_ISL(constellation)  # 清空现有的所有ISL
        function = self.plugins[self.current_connection_mode]
        function(constellation , t)  # 转去执行相应的连接模式函数来建立对应的ISL

