import numpy as np
from Model.Node import Node
from Model.Wires import Wire, Wires
from Model.Ground import Ground


if __name__ == '__main__':
    # 初始化节点数据
    node1 = Node('X01', 0, 0, 10.5)
    node2 = Node('X02', 1000, 0, 10.5)
    node3 = Node('X03', 0, -0.4, 10)
    node4 = Node('X04', 1000, -0.4, 10)
    node5 = Node('X05', 0, 0.1, 10)
    node6 = Node('X06', 1000, 0.1, 10)
    node7 = Node('X07', 0, 0.6, 10)
    node8 = Node('X08', 1000, 0.6, 10)

    # 初始化向量拟合参数
    frq = np.concatenate([
        np.arange(1, 91, 10),
        np.arange(100, 1000, 100),
        np.arange(1000, 10000, 1000),
        np.arange(10000, 100000, 10000),
        np.arange(100000, 1000000, 100000),
        np.arange(1000000, 10000000, 1000000),
        np.arange(10000000, 100000000, 10000000),
        np.arange(100000000, 1000000000, 100000000)
    ])
    VF = {'odc': 10,
          'frq': frq}

    # 根据节点连接成线段
    wire1 = Wire('Y01', node1, node2, 0, 0.005, 0, 0, 58000000, 1, 1, VF)
    wire2 = Wire('Y02', node3, node4, -0.4, 0.005, 0, 0, 58000000, 1, 1, VF)
    wire3 = Wire('Y03', node5, node6, 0.1, 0.005, 0, 0, 58000000, 1, 1, VF)
    wire4 = Wire('Y04', node7, node8, 0.6, 0.005, 0, 0, 58000000, 1, 1, VF)

    # 创建地面对象
    ground = Ground(1e-3, 1, 4, 'LSG', 'weak', 'isolational')





    
