class Cable:
    def __init__(self, Info, Wires, Ground, Measurement):
        """
        初始化电缆对象

        参数:
        Info (CableInfo): 电缆自描述信息对象
        Wires (Wires): 电缆线段对象集合
        Ground (Ground): 电缆地线对象集合
        Measurement (Measurement): 电缆测量对象集合
        """
        self.info = Info
        self.wires = Wires
        self.ground = Ground
        self.measurement = Measurement