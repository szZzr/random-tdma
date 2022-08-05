import queue
class Map:
    def __init__(self):
        self.nodes = {}
        self.channels = set()

    def insert_node(self, name, trans, rec):
        node  = (trans, rec)
        self.nodes.update({name:node})
        self.channels.update(trans,[rec])

    def get_channels(self)->list:
        return list(self.channels)

    def channel_nodes(self, channel: int=0):
        if channel is 0:
            return list(self.nodes.keys())
        else: #No case, yet!
            return []

    def get_num_nodes(self)->int:
        return len(self.nodes.values())

    def show(self, prefix:str='', end:str='\n\n'):
        print(f'{prefix}', end='')
        for node in self.nodes.keys():
            print(f'Node-{node}: Transmit->{self.nodes[node][0]}, Receive->{self.nodes[node][1]}')
        print(f'channels : {self.channels}',end=f'{end}')

    def get_node(self, name:int):
        return self.nodes[name]
