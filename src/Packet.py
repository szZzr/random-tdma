from Message import Message, NullMessage
class Slot:
    def __init__(self, channel:int, source:int, data:Message):
        self.channel = channel
        self.source = source
        self.data = data

class Packet:
    def __init__(self, size:int=0):
        self.size = size
        self.channels = []
        self.nodes = []
        self.data = []

    def __iter__(self):
        self.it = 0
        return self

    def __next__(self):
        it = self.it
        self.it += 1
        if it < self.size:
            return self.get_slot(it)
        else:
            raise StopIteration

    def get_slot(self, index:int):
        return Slot(self.channels[index], self.nodes[index], self.data[index])

    def _exist_node_(self, node: int):
        if node in self.nodes:
            return True
        else:
            exec(f'Node-{node} not found in current packet.')

    def _has_space_(self):
        return  len(self.nodes) < self.size

    def add_slot(self,node:int, channel:int):
        if not self._has_space_():
            exec(f'Slots are full.\nNode-{node} has been rejected.')
        self.channels.append(channel)
        self.nodes.append(node)
        self.data.append(0)

    def _remove_slot_(self, slot):
        self.channels.pop(slot)
        self.nodes.pop(slot)
        self.data.pop(slot)
        self.size -= 1

    def add_data(self, node:int, data:Message):
        if isinstance(data, NullMessage):
            index = self.nodes.index(node)
            self._remove_slot_(index)
            return
        self._exist_node_(node)
        index = self.nodes.index(node)
        self.data[index] = data

    def get_data(self, node:int):
        self._exist_node_(node)
        index = self.nodes.index(node)
        return self.data[index]

    def is_init(self)->bool:
        #TODO: Case for no packets !!!
        if self.size != 0:
            return True
        else:
            exec('No packet exist.')

    def is_completed(self):
        # self._filtering_()
        # self.is_init()
        for d in self.data:
            if d is 0:
                return False

        return True

    def show(self):
        print(f'size: {self.size}, channels: {self.channels}, nodes: {self.nodes}, data: {self.data}')

    def get_size(self)->int:
        return self.size
