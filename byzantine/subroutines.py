from netqasm.sdk.external import NetQASMConnection, Socket
from netqasm.sdk import EPRSocket
from random import randint

class Routine:
    def __init__(self, socket: list, epr_socket: list, bi: int):
        self._sockets = socket
        self._epr_socket = epr_socket
        self._bi = bi
        self.other_bi = []
        self.result=-1
        k=2
    
    def subroutine_1(self):
        self.other_bi = []
        for socket in self._sockets:

            socket.send(str(self._bi))
            self.other_bi.append(int(socket.recv()))
        print("subroutine_1")
        x= sum(self.other_bi)
        if x < (len(self.other_bi)+1)/3:
            self._bi=0
        elif x> (2*len(self.other_bi)+1)/3:
            self._bi=1
        else:
            bi= randint(0,1) #QOCC
    def subroutine_2(self):
        print("subroutine_2")
        self.other_bi = []
        for socket in self._sockets:

            socket.send(str(self._bi))
            self.other_bi.append(int(socket.recv()))
        x= sum(self.other_bi)
        if x < (len(self.other_bi)+1)/3:
            return 0
        elif x> (2*len(self.other_bi)+1)/3:
            self._bi=1
        
    def subroutine_3(self):
        print("subroutine_3")
        self.other_bi = []
        for socket in self._sockets:

            socket.send(str(self._bi))
            self.other_bi.append(int(socket.recv()))
        x= sum(self.other_bi)
        if x < (len(self.other_bi)+1)/3:
            self._bi=0
        elif x> (2*len(self.other_bi)+1)/3:
            return 1
    def start_routine(self):
        while True:
            self.subroutine_1()
            if self.subroutine_2()==0:
                self.result=0
                break
            elif self.subroutine_3()==1:
                self.result=1
                break
            
