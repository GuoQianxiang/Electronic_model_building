class OHL:
    def __init__(self, wires, Info, ground, Measurement):
        """
        初始化架空线对象

        参数:
        wires (Wires): 架空线线段对象集合
        Info (OHLInfo): 架空线自描述信息对象
        ground (Ground): 架空线地线对象集合
        Measurement (Measurement): 架空线测量对象集合
        """
        self.wires = wires
        self.info = Info
        self.ground = ground
        self.measurement = Measurement