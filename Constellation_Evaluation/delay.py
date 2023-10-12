'''

作者 ： 侯玉南

日期 ： 2023年8月25日09:09:14

功能 ： 在指定的星座连接方式、路由策略下，计算两个通信端点之间的延迟

'''
import numpy as np
import networkx as nx
from math import radians, cos, sin, asin, sqrt
import plotly.graph_objects as go



# 计算地面站与一颗卫星之间的距离（计算结果考虑了地球的曲率），返回值的单位是千米
def distance_between_satellite_and_groundstation(groundstation , satellite):
    longitude1 = groundstation.longitude
    latitude1 = groundstation.latitude
    longitude2 = satellite.longitude
    latitude2 = satellite.latitude
    longitude1,latitude1,longitude2,latitude2 = map(radians, [float(longitude1), float(latitude1), float(longitude2), float(latitude2)]) # 经纬度转换成弧度
    dlon=longitude2-longitude1
    dlat=latitude2-latitude1
    a=sin(dlat/2)**2 + cos(latitude1) * cos(latitude2) * sin(dlon/2)**2
    distance=2*asin(sqrt(a))*6371.0*1000 # 地球平均半径6371km
    distance=np.round(distance/1000,3)  # 将结果转化为千米为单位，保留三位小数
    return distance



# 传入参数含义 ： constellation_name是星座名称,参数类型是字符串,如"Starlink"
# shell是星座中的某一层shell,字符串类型,如"shell_1","shell_2","shell_3",……的形式给出,表示星座中的第几个shell，如"shell_1"表示第一层shell
# source是源地面站,target是目标地面站,t表示某一个时隙（timeslot）
# sh是一个shell类对象，表示星座中的一个shell
def delay(constellation_name , shell , source , target , t , sh):
    # 读取constellation星座的shell层的延迟矩阵
    with open("Constellation_Connection/Constellation_Snapshot/" + \
              constellation_name + "/delay/" + shell + "/timeslot_" + str(t) + ".txt", 'r') as file:
        lines = file.readlines()
        data = [line.strip().split() for line in lines]
    delay = [] # 存放从文件读取出来的延迟数据
    for row in data:
        row_data = [float(value) for value in row]
        delay.append(row_data)

    # 找到距离源地面站最近的卫星
    nearest_satellite_to_source_groundstation = None # 距离源地面站最近的卫星
    satellite_to_source_groundstation_distance = float('inf') # 初始化到达源基站最近的距离为无穷大
    nearest_satellite_to_target_groundstation = None # 距离目标地面站最近的卫星
    satellite_to_target_groundstation_distance = float('inf') # 初始化到达目标基站最近的距离为无穷大
    # 遍历sh层shell中的每一颗卫星
    for orbit in sh.orbits :
        for satellite in orbit.satellites:
            dis1 = distance_between_satellite_and_groundstation(source , satellite) # 计算当前遍历到的卫星与源地面站的距离
            dis2 = distance_between_satellite_and_groundstation(target , satellite) # 计算当前遍历到的卫星与目标地面站的距离
            if dis1 < satellite_to_source_groundstation_distance :
                satellite_to_source_groundstation_distance = dis1
                nearest_satellite_to_source_groundstation = satellite
            if dis2 < satellite_to_target_groundstation_distance :
                satellite_to_target_groundstation_distance = dis2
                nearest_satellite_to_target_groundstation = satellite

    # 上面的for循环结束后，变量nearest_satellite_to_source_groundstation就表示距离源地面站最近的卫星，
    # nearest_satellite_to_target_groundstation就表示距离目标地面站最近的卫星

    G = nx.Graph() # 创建一个名为G的无向图对象，一开始是空的，没有节点和边
    satellite_nodes = []
    for i in range(1 , len(delay) , 1):
        satellite_nodes.append("satellite_" + str(i))
    G.add_nodes_from(satellite_nodes)  # 向无向图中添加节点

    satellite_edges = []
    edge_weights = []
    for i in range(1 , len(delay) , 1):
        for j in range(i+1 , len(delay) , 1):
            if delay[i][j] > 0:
                satellite_edges.append(("satellite_" + str(i) , "satellite_" + str(j) , delay[i][j]))
                edge_weights.append(delay[i][j])
    G.add_weighted_edges_from(satellite_edges) # 向无向图中添加边，边的权重就是delay矩阵中的数值

    # 以下注释中的内容为可视化部分代码
    '''
    edges = G.edges()
    # ## update to 3d dimension
    spring_3D = nx.spring_layout(G, dim=3, k=0.5)  # k regulates the distance between nodes
    # weights = [G[u][v]['weight'] for u,v in edges]
    # nx.draw(G, with_labels=True, node_color='skyblue', font_weight='bold',  width=weights, pos=pos)

    # we need to seperate the X,Y,Z coordinates for Plotly
    # NOTE: spring_3D is a dictionary where the keys are 1,...,6
    x_nodes = [spring_3D[key][0] for key in spring_3D.keys()]  # x-coordinates of nodes
    y_nodes = [spring_3D[key][1] for key in spring_3D.keys()]  # y-coordinates
    z_nodes = [spring_3D[key][2] for key in spring_3D.keys()]  # z-coordinates

    # we need to create lists that contain the starting and ending coordinates of each edge.
    x_edges = []
    y_edges = []
    z_edges = []

    # create lists holding midpoints that we will use to anchor text
    xtp = []
    ytp = []
    ztp = []

    # need to fill these with all of the coordinates
    for edge in edges:
        # format: [beginning,ending,None]
        x_coords = [spring_3D[edge[0]][0], spring_3D[edge[1]][0], None]
        x_edges += x_coords
        xtp.append(0.5 * (spring_3D[edge[0]][0] + spring_3D[edge[1]][0]))

        y_coords = [spring_3D[edge[0]][1], spring_3D[edge[1]][1], None]
        y_edges += y_coords
        ytp.append(0.5 * (spring_3D[edge[0]][1] + spring_3D[edge[1]][1]))

        z_coords = [spring_3D[edge[0]][2], spring_3D[edge[1]][2], None]
        z_edges += z_coords
        ztp.append(0.5 * (spring_3D[edge[0]][2] + spring_3D[edge[1]][2]))

    etext = [f'weight={w}' for w in edge_weights]

    trace_weights = go.Scatter3d(x=xtp, y=ytp, z=ztp,
                                 mode='markers',
                                 marker=dict(color='rgb(125,125,125)', size=1),
                                 # set the same color as for the edge lines
                                 text=etext, hoverinfo='text')

    # create a trace for the edges
    trace_edges = go.Scatter3d(
        x=x_edges,
        y=y_edges,
        z=z_edges,
        mode='lines',
        line=dict(color='black', width=2),
        hoverinfo='none')

    # create a trace for the nodes
    trace_nodes = go.Scatter3d(
        x=x_nodes,
        y=y_nodes,
        z=z_nodes,
        mode='markers',
        marker=dict(symbol='circle',
                    size=10,
                    color='skyblue')
    )

    # Include the traces we want to plot and create a figure
    data = [trace_edges, trace_nodes, trace_weights]
    fig = go.Figure(data=data)

    fig.show()
    '''

    start_satellite = "satellite_" + str(nearest_satellite_to_source_groundstation.id)  # 起始路由卫星的编号
    end_satellite = "satellite_" + str(nearest_satellite_to_target_groundstation.id)  # 终止路由卫星的编号

    # 求最短路径
    path = nx.dijkstra_path(G, source=start_satellite, target=end_satellite)
    # 打印路径
    #print(path)
    # 求最短延迟时间（秒）
    length = 0
    for i in range(len(path) - 1):
        length += G.edges[path[i], path[i + 1]]['weight']

    return length



