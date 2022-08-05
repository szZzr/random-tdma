import time
COUPLER:int = 0
NO_RECEIVER:int = -1

class Message:
    def __init__(self, source:int, destination:int, clock_time:int=0):
        self.source:int = source
        self.destination:int = destination
        self.gen_time = clock_time # Generating time (hops)
        self.arr_time = -1 # Arrived time (hops)
        self.time = time.gmtime()


    def show(self, prefix:str=''):
        print(f'{prefix}Source: {self.source}, Destination: {self.destination} Message: {self.time}\n\n')


class HelloMessage(Message):
    def __init__(self, source:int, trans:list, rec:list):
        super().__init__(source, COUPLER)
        self.trans = trans
        self.rec = rec

    def show(self):
        super().show()
        print(f'Transmit: {self.trans}\nReceive: {self.rec}')


class WelcomeMessage(Message):
    def __init__(self, destination: int):
        super().__init__(COUPLER, destination)


class NullMessage(Message):
    def __init__(self, source: int):
        super().__init__(source, NO_RECEIVER)


