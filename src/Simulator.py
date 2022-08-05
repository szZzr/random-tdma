from Node import Node
from Coupler import Coupler

def nodes_creator()->(dict, dict):
    '''
    Nodes initialize function.
    :return:
    '''
    rec = {1:1,2:1,3:2,4:2,5:3,6:3,7:4,8:4}
    trans = [1,2,3,4]
    directory = {1:(1,2), 2:(3,4), 3:(5,6), 4:(7,8)}
    return {i+1:Node(i+1, trans, rec[i+1]) for i in range(8)}, directory


def nodes_generate_messages(nodes:list, possibility:float, rec:dict, time:int):
    '''
    Generates new messages for every node of given list
    with given possibility.
    :param nodes: List of Node
    :param possibility: Float, denotes generator possibility.
    :return:
    '''
    for node in nodes:
        node.generator_messages(possibility,rec, time)



def simulate(coupler: Coupler, nodes:dict, time:int=0)->int:
    '''
    Simulation procedure.
    :param coupler: Star Coupler
    :param nodes: All nodes
    :return:
    '''
    coupler.new_packet()
    i_selections = coupler.selected_nodes()
    s_nodes = [nodes[i] for i in i_selections]
    coupler.receive_data(s_nodes, time)

    # print(f'{round+1})',end='')
    # coupler.current_packet.show()

    packet_size = coupler.current_packet.get_size()
    coupler.transmit_data(nodes, time)
    return packet_size


def get_nodes_stats(nodes:list)->dict:
    delayed_trans = 0
    delayed_messages = 0
    waiting_nodes = 0 # Number of nodes that have a message to send and waiting their turn
    for node in nodes:
        msgs = node.delayed_messages()
        delayed_trans += node.delayed_outgoing()
        delayed_messages += msgs
        if msgs >0:
            waiting_nodes += 1
    return {'delayed_messages': delayed_messages,
            'waiting': waiting_nodes,
            'delayed_trans':delayed_trans}

# def get_delay(nodes:list)->float:
#     if not nodes: #is empty
#         return 0.0
#     waiting_time = 0
#     for node in nodes:
#         waiting_time += node.average_waiting_time()
#     return waiting_time/len(nodes)

def get_delay(nodes:list)->float:
    if not nodes: #is empty
        return 0.0
    waiting_time = 0
    for node in nodes:
        # print(f'{node.name}) total-delayed: {node.total_delayed}, received: {node.received}')
        waiting_time += node.total_delayed//node.received
    return waiting_time/len(nodes)

def get_nodes_delivered_messages(nodes:list)->int:
    delivered = 0
    for node in nodes:
        delivered += node.delivered_messages()
    print(f'Delivered: {delivered}')
    return delivered


def run(rounds:int, possibility:float):
    the_stats = {'delayed_messages':0, 'transmitted':0, 'waiting':0, 'delayed_trans':0}
    nodes, rec_catalog = nodes_creator()
    star= Coupler(channels=4, nodes=len(nodes))
    star.mapping(list(nodes.values()))
    # star.map.show()
    for clock in range(rounds):
        nodes_generate_messages(list(nodes.values()), possibility, rec_catalog, clock)
        # the_stats['transmitted'] += simulate(star, list(nodes.values()))
        the_stats['transmitted'] += simulate(star, nodes, clock)

        stats = get_nodes_stats(list(nodes.values()))
        the_stats['delayed_messages'] += stats['delayed_messages']
        the_stats['waiting'] += stats['waiting']
        the_stats['delayed_trans'] += stats['delayed_trans']

    return {'delayed_messages': the_stats['delayed_messages'],
            'transmitted':the_stats['transmitted'],
            'waiting':the_stats['waiting'],
            'delayed_trans':the_stats['delayed_trans'],
            'delivered':get_nodes_delivered_messages(list(nodes.values())),
            'average_waiting_time': get_delay(list(nodes.values()))}
