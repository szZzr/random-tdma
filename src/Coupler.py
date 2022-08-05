import random
from Map import Map
from Packet import Packet

class Coupler:
    def __init__(self, channels:int, nodes:int):
        self.channels = channels
        self.nodes = nodes
        self.map:Map = Map()
        self.current_packet = Packet()

    def _random_heap_(self, heap:list):
        return random.choice(range(0,len(heap)))

    def mapping(self, nodes_to_connect:list)-> None:
        for node in nodes_to_connect:
            msg = node.connect_coupler()
            self.map.insert_node(msg.source, msg.trans, msg.rec)

    def new_packet(self)-> None:
        '''
        Initialized a new Packet with default settings. After that
        selects a random channel for each slot, and for this channel
        selects randomly a node to transmit his message. Finally, defines
        this packet as the current coupler's packet.
        :return: None
        '''
        packet = Packet(self.channels)
        channels =  self.map.get_channels()
        # candidates = {c:self.map.channel_nodes(c) for c in channels}
        candidates = self.map.channel_nodes()
        while not not channels:
            c = channels.pop(self._random_heap_(channels)) # Choose at random one channel
            trans_i = candidates.pop(self._random_heap_(candidates)) # Choose at random one node
            packet.add_slot(node=trans_i, channel=c)
        self.current_packet = packet

    def selected_nodes(self)->list:
        '''
        :return: List of integer with selected nodes.
        '''
        if self.current_packet.is_init():
            nodes = self.current_packet.nodes
            return nodes

    def _nodes_filtering_(self, nodes, names_in_use)->list:
        i = 0
        while i<len(nodes):
            if nodes[i].name not in names_in_use:
                nodes.pop(i)
            else:
                i += 1
        return nodes


    def receive_data(self, source_nodes:list, time:int)->list:
        '''
        If the selected node for each channel, has a message for this channel
        the coupler received a Message, otherwise if this node's buffer for the
        selected channel is empty then a NullMessage will Coupler received and
        then the packet will reduce by one its slots. Finally will returns a list
        of nodes which their message is not a NullMessage.
        :param nodes: List of instances of class Node
        :return: List of instances of class Node
        '''
        if self.current_packet.is_init():
            channels = self.current_packet.channels.copy()
            for i, node in enumerate(source_nodes):
                # node.display_outgoing('\t\t-*')
                data = node.send_message(channels[i], time)
                # node.display_outgoing('\t\t\t->')
                self.current_packet.add_data(node.name, data)
        else:
            exec('Packet is not initialized.')
        return self._nodes_filtering_(source_nodes, self.current_packet.nodes)

    def receive_data_random(self, nodes:list)->list: #NOT USED
        '''
        ***This method doesn't used for the running example.***

        :param nodes:
        :return:
        '''
        if self.current_packet.is_init():
            for node in nodes:
                data = node.send_message_random()
                self.current_packet.add_data(node.name, data)
        else:
            exec('Packet is not initialized.')
        results = self._nodes_filtering_(nodes, self.current_packet.nodes)
        return results


    def transmit_data(self, nodes:dict, time:int):
        if self.current_packet.is_completed():
            it = iter(self.current_packet)
            for slot in it:
                msg = slot.data
                destination = nodes[msg.destination] #instance of class Node
                # msg.show('\t ') # Display Message
                destination.receive_message(msg, time)
                # destination.display_incoming('\t\t') # Display destination nodes incoming messages
            self.end_of_transmission()
        else:
            exec('Transmission failed!\nPacket is not completed.')



    def end_of_transmission(self):
        self.current_packet = Packet()


