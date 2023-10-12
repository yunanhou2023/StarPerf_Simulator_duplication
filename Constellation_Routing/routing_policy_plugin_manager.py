'''

作者 ： 侯玉南

日期 ： 2023年8月24日19:59:52

功能 : 该文件定义了关于星座路由策略的管理器类，这是一个开放性接口，可以很容易地接入任何路由策略，比如OSPF、RIP等
       该类采用单例模式，整个项目中从始至终只允许有一个管理器出现
       后续如果想加入新的路由策略，只需要按照接口规范文档编写函数就可以了
       要求 ： Routing_Plugin文件夹下存放的均为本项目所有的路由策略，每个py文件包含一个函数，一个函数就是一个路由策略的定义，函数名与文件名相同

目前的疑问：像OSPF、RIP这些路由策略不应该该是提供IP地址才可以实现吗？
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
class routing_policy_plugin_manager:
    def __init__(self):
        self.plugins = {}  # 路由策略插件字典，存放本项目中所有的路由策略插件，字典的key是路由策略的函数名称，value是路由策略对应的函数
        # 下面的代码块用来遍历Routing_Plugin文件夹，该文件夹存放的是所有路由策略的py文件
        # 遍历这个文件夹获取所有的路由策略插件的名称，存放到self.plugins集合中
        package_name = "Constellation_Routing.Routing_Plugin"
        plugins_path = package_name.replace(".", os.path.sep)  # 插件存放的路径
        for plugin_name in os.listdir(plugins_path):
            if plugin_name.endswith(".py"):
                plugin_name = plugin_name[:-3]  # 去掉文件扩展名.py
                plugin = importlib.import_module(package_name + "." + plugin_name)
                if hasattr(plugin, plugin_name) and callable(getattr(plugin, plugin_name)):
                    function = getattr(plugin, plugin_name)
                    self.plugins[plugin_name] = function
        self.current_routing_policy = "OSPF"  # 设置当前路由策略插件管理器使用的路由策略，默认采用OSPF路由策略

    # 切换路由策略，参数含义 ： plugin_name是新路由策略的名称
    def set_routing_policy(self, plugin_name):
        self.current_routing_policy = plugin_name  # 将当前路由策略设置为指定策略
        print("当前星座路由策略已切换为 " + plugin_name)

    # 执行路由算法 ： 执行当前管理器指定的路由策略，即执行self.current_routing_policy所指示的路由策略
    def execute_routing_policy(self , constellation):
        function = self.plugins[self.current_routing_policy]
        function(constellation)  # 转去执行相应的路由策略函数