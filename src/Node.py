import queue, random
from Message import Message, HelloMessage, NullMessage, COUPLER


class Node:
    def __init__(self,name:int, trans, rec, buf_size=4):
        self.name:int = name
        self.trans = trans
        self.rec = rec
        self.buffer:dict= {f'{c}':queue.Queue(maxsize=buf_size) for c in trans}
        self.incoming = []
        self.outgoing = set() # channels that have outgoing messages
        self.delivered = 0
        self.waiting_time = 0
        self.received = 0
        self.total_delayed = 0

    def _random_channel_(self, not_empty:bool=False)->int:
        '''
        Selects randomly a channel of trans list.
        :param not_empty: If it is false, select a channel from his self.trans list.
        :return: Randomly a channel from the same list where its buffer is not empty.
        '''
        if not not_empty:
            return random.choice(self.trans)
        else:
            # fill_trans = self.trans
            # for t in fill_trans:
            #     if self.buffer[f'{t}'].empty():
            #         fill_trans.pop(fill_trans.index(t))
            return random.choice(list(self.outgoing))

    def _new_message_(self,receivers:dict, time:int):
        c: int = self._random_channel_()
        dest: int = random.choice(receivers[c])
        buffer = self.buffer[f'{c}']
        if buffer.full():
            buffer.get() #Drops the first msg
        buffer.put(
            Message(source=self.name, destination=dest, clock_time=time)
        )
        self.outgoing.add(c)

    def generator_messages(self, possibility: float, receivers:dict, time:int):
        p = random.choices([0,1], [(1-possibility)*100,possibility*100])[0]
        if p==1:
            self._new_message_(receivers, time)


    # def abstract_generator(self,possibility: float, receivers:dict, time:int):
    #     p = random.choices([0, 1], [(1 - possibility) * 100, possibility * 100])[0]
    #     if p == 1:


    def _get_channel_msg_(self,channel)->Message:
        buffer = self.buffer[f'{channel}']
        if not buffer.empty():
            msg: Message = buffer.get()
            # buffer.queue.clear() # Send all messages of a specific channel
            if buffer.empty(): # First checks if channel's buffer is empty and then remove it from outgoing[set]
                self.outgoing.remove(channel)
            return msg
        else:
            return NullMessage(source=self.name)
            # raise Exception(f'Node-{self.name}: Empty queue-{channel}.')

    def send_message(self, channel:int, time:int)->Message:
        '''
        For a specified channel, verify that has a message,
        and if it's true send the message, otherwise response
        with a NullMessage
        :param channel: Specified channel (int)
        :return: Message
        '''
        if not self.outgoing: #there are not outgoing message
            return NullMessage(source=self.name)
        msg = self._get_channel_msg_(channel=channel)
        self.delivered += 1
        self.waiting_time += time - msg.gen_time
        return msg

    def send_message_random(self)->Message: #NOT USED
        if not self.outgoing: #there are not outgoing message
            return NullMessage(source=self.name)
        dest:int = self._random_channel_(not_empty=True)
        msg = self._get_channel_msg_(channel=dest)
        return msg

    def receive_message(self, msg: Message, time:int):
        if msg.destination is self.name:
            msg.arr_time = time
            self.incoming.append(msg)

            # Stats
            self.received += 1
            self.total_delayed += msg.arr_time - msg.gen_time
            # print(f'{self.name}: Rec-from-{msg.source}, delay:{msg.arr_time - msg.gen_time}')

    def connect_coupler(self)->HelloMessage:
        return HelloMessage(self.name, self.trans, self.rec)


    def delayed_messages(self)->int:
        '''
        Access all node's buffers and count the number
        of delayed messages.
        :return: Total number of delayed messages
        '''
        delayed = 0
        for q in self.buffer.values():
            delayed += q.qsize()
        return delayed

    def delayed_outgoing(self)->int:
        return len(self.outgoing)

    def display_incoming(self,prefix:str=''):
        print(f'{prefix}Node-{self.name} - [{len(self.incoming)}]:', end='')
        for msg in self.incoming:
            print(f'{msg}', end=', ')
        print('\n')

    def display_outgoing(self, prefix:str='', end:str='\n'):
        print(f'{prefix}Node-{self.name} - [{len(self.outgoing)}]: {self.outgoing}',end=f'{end}')


    def delivered_messages(self):
        return self.delivered

    def average_waiting_time(self):
        if self.delivered == 0:
            return 0
        return self.waiting_time/self.delivered
