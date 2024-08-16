import numpy as np
from Driver.initialization.initialization import initialize_tower
from Driver.modeling.tower_modeling import tower_building


if __name__ == '__main__':
    # 变频下的频率矩阵
    frq = np.concatenate([
        np.arange(1, 91, 10),
        np.arange(100, 1000, 100),
        np.arange(1000, 10000, 1000),
        np.arange(10000, 100000, 10000)
    ])
    VF = {'odc': 10,
          'frq': frq}
    # 固频的频率值
    f0 = 2e4
    # 线段的最大长度, 后续会按照这个长度, 对不符合长度规范的线段进行切分
    max_length = 50

    tower = initialize_tower(file_name = "01_2",
                             max_length = max_length)

    tower_building(tower, f0, max_length)