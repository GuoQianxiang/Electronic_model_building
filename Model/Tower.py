class Tower:
    def __init__(self, Info, Wires, Lump, Ground, Device, MeasurementNode):
        """
        初始化杆塔对象

        参数:
        Info (TowerInfo): 杆塔自描述信息对象
        Wires (Wires): 杆塔线段对象集合
        Lump (Lump): 集中参数对象集合
        Ground (Ground): 杆塔地线对象集合
        Device (Device): 杆塔设备对象集合
        MeasurementNode (MeasurementNode): 杆塔测量节点对象集合

        无需传入的参数：
        nodes (list): 杆塔结点名字列表
        brans (list): 杆塔线段名字列表
        """
        self.info = Info
        self.wires = Wires
        self.lump = Lump
        self.ground = Ground
        self.device = Device
        self.measurementNode = MeasurementNode
        self.nodes = Wires.get_node_names()
        self.brans = Wires.get_node_coordinates()