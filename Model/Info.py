class Info:
    def __init__(self, name, ID, Type):
        """
        初始化自描述信息对象
        
        参数:
        name (str): 模型的名称
        ID (int): 模型的ID
        Type (str): 模型的类型
        """
        self.name = name
        self.ID = ID
        self.Type = Type


class TowerInfo(Info):

    def __init__(self, Tower_name, Tower_ID, Tower_Type, Tower_Vclass, Center_Node, Theta, Mode_Con, Mode_Gnd, Pole_Height, Pole_Head_Node):
        """
        初始化杆塔自描述信息对象
        
        参数:
        name (str): 杆塔名
        ID (int): 序号
        Type (str): 杆塔类型
        Tower_Vclass (str): 杆塔电压等级
        Center_Node (Node(name, x, y, z)): 中心节点
        Theta (float): 杆塔偏转角度
        Mode_Con (int): VF设置
        Mode_Gnd (int): 镜像VF设置
        Pole_Height (float): 杆塔高度
        Pole_Head_Node (Node(name, x, y, z)): 杆塔头节点
        """
        super().__init__(Tower_name, Tower_ID, Tower_Type)
        self.Tower_Vclass = Tower_Vclass
        self.Center_Node = Center_Node
        self.Theta = Theta
        self.Mode_Con = Mode_Con
        self.Mode_Gnd = Mode_Gnd
        self.Pole_Height = Pole_Height
        self.Pole_Head_Node = Pole_Head_Node

class OHLInfo(Info):
    def __init__(self, OHL_name, OHL_ID, OHL_Type, dL, model1, model2, HeadTower, TailTower):
        """
        初始化杆塔自描述信息对象
        
        参数:
        name (str): 架空线名称
        ID (int): 架空线序号
        Type (str): 架构线类型
        dL (float): 元线段长度
        model1 (str): 架空线模型1
        model2 (str): 架空线模型2
        HeadTower (str): 架空线头杆塔
        TailTower (str): 架空线尾杆塔

        """
        super().__init__(OHL_name, OHL_ID, OHL_Type)
        self.dL = dL
        self.model1 = model1
        self.model2 = model2
        self.HeadTower = HeadTower
        self.TailTower = TailTower
