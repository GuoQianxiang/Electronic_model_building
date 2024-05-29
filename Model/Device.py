class Device:
    def __init__(self, ins, sar, txf):
        self.INS = ins
        self.SAR = sar
        self.TXF = txf

    
    def __repr__(self):
        """
        返回对象的字符串表示形式。
        """
        return f"Device(INS={self.INS}, SAR={self.SAR}, TXF={self.TXF})"