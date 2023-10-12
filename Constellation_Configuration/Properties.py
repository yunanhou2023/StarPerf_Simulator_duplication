'''

作者 ： 侯玉南

日期 ： 2023年8月25日19:03:33

功能 ： 该文件定义了读取.properties文件的类，用于读取星座属性配置文件

'''

# 读取Properties文件类
class Properties:
    def __init__(self, file_name):
        self.file_name = file_name

    def getProperties(self):
        try:
            pro_file = open(self.file_name, 'r', encoding='utf-8')
            properties = {}
            for line in pro_file:
                if line.find('=') > 0:
                    strs = line.replace('\n', '').split('=')
                    properties[strs[0]] = strs[1]
        except Exception as e:
            raise e
        else:
            pro_file.close()
        return properties
