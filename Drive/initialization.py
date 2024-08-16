import json
import numpy as np
from Model.Node import Node
from Model.Wires import Wire, Wires, CoreWire, TubeWire
from Model.Ground import Ground
from Model.Tower import Tower

def connect_nodes(nodes,pos_wire):
    for node in nodes:
        pos = [node.x, node.y, node.z]
        if pos_wire == pos:
            return node
    return False

# initialize wire in tower
def initialize_wire(wire, nodes):
    bran = wire['bran']
    node_name_start = wire['node1']
    pos_start = wire['pos_1']
    node_name_end = wire['node2']
    pos_end = wire['pos_2']
    node_start = Node(node_name_start, pos_start[0], pos_start[1], pos_start[2])
    node_end = Node(node_name_end, pos_end[0], pos_end[1], pos_end[2])
    connect_start = connect_nodes(nodes,node_start)
    connect_end = connect_nodes(nodes, node_end)

    if connect_start:
        node_start = connect_start
    else:
        nodes.append(node_start)

    if connect_end(nodes, node_end):
        node_end = connect_end
    else:
        nodes.append(node_end)

    offset = wire['oft']
    radius = wire['r0']
    R = wire['r']
    L = wire['l']
    sig = wire['sig']
    mur = wire['mur']
    epr = wire['epr']
    # 自定义一个VF
    # 初始化向量拟合参数
    frq = np.concatenate([
        np.arange(1, 91, 10),
        np.arange(100, 1000, 100),
        np.arange(1000, 10000, 1000),
        np.arange(10000, 100000, 10000),
    ])
    VF = {'odc': 10,
          'frq': frq}
    if wire['type'] == 'air' or wire['type'] == 'sheath' or wire['type'] == 'ground':
        return Wire(bran, node_start, node_end, offset, radius, R, L, sig, mur, epr, VF)
    elif wire['type'] == 'core':
        return CoreWire(bran, node_start, node_end, offset, radius, R, L, sig, mur, epr, VF, wire['rs2'], wire['rs3'])


# initialize ground in tower
def initialize_ground(ground_dic):
    sig = ground_dic['sig']
    mur = ground_dic['mur']
    epr = ground_dic['epr']
    model = ground_dic['gnd_model']
    ionisation_intensity = ground_dic['ionisation_intensity']
    ionisation_model = ground_dic['ionisation_model']

    return Ground(sig, mur, epr, model, ionisation_intensity, ionisation_model)


def initialize_tower(file_name):
    json_file_path = "Data/" + file_name + ".json"
    # 0. read json file
    with open(json_file_path, 'r') as j:
        load_dict = json.load(j)

    # 1. initialize wires
    wires = Wires()
    nodes = []
    for wire in load_dict['Tower']['Wire']:

        # 1.1 initialize air wire
        if wire['type'] == 'air':
            wire_air = initialize_wire(wire, nodes)
            wires.add_air_wire(wire_air)  # add air wire in wires

        # 1.2 initialize ground wire
        elif wire['type'] == 'ground':
            wire_ground = initialize_wire(wire)
            wires.add_ground_wire(wire_ground)  # add ground wire in wires

        # 1.3 initialize tube
        elif wire['type'] == 'tube':
            sheath_wire = initialize_wire(wire['sheath'])
            tube_wire = TubeWire(sheath_wire, wire['sheath']['rs2'], wire['sheath']['rs3'], wire['sheath']['num'])

            for core in wire['core']:
                core_wire = initialize_wire(core)
                tube_wire.add_core_wire(core_wire)

            wires.add_tube_wire(tube_wire)  # add tube in wires

    # ---对所有线段进行切分----
    max_length = 50
    wires.display()
    wires.split_long_wires_all(max_length)
    wires.add_air_wire(sheath_wire)  # sheath wire is in the air, we need to calculate it in air part.

    # 2. initialize ground
    ground_dic = load_dict['Tower']['ground']
    ground = initialize_ground(ground_dic)

    # 3. initalize tower
    tower = Tower(None, wires, None, ground, None, None, )
    print("tower loaded")
    return tower

