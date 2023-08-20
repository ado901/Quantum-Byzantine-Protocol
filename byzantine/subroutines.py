from netqasm.sdk.external import NetQASMConnection, Socket
from netqasm.sdk import EPRSocket,Qubit
from random import randint

class Routine:
    def __init__(self, socket: list[Socket], epr_socket: list[EPRSocket], bi: int, name:str):
        self._name= name
        self._sockets = socket
        self._epr_socket = epr_socket
        self._bi = bi
        self.other_bi = []
        self.result=-1
        k=2
    
    def subroutine_1(self):
        print(f"subroutine_1 for {self._name}")
        x=0
        for socket in self._sockets:
            
            socket.send(str(self._bi))
            x+=int(socket.recv())
        print(f"subroutine_1 for {self._name} is {x}")
        if x < (len(self.other_bi)+1)/3:
            self._bi=0
        elif x> (2*len(self.other_bi)+1)/3:
            self._bi=1
        else:
            bi= randint(0,1) #QOCC
    def subroutine_2(self):
        print(f"subroutine_2 for {self._name}")
        x=0
        self.other_bi = []
        for socket in self._sockets:

            socket.send(str(self._bi))
            x+=int(socket.recv())
        if x < (len(self.other_bi)+1)/3:
            return 0
        elif x> (2*len(self.other_bi)+1)/3:
            self._bi=1
        
    def subroutine_3(self):
        print(f"subroutine_3 for {self._name}")
        x=0
        self.other_bi = []
        for socket in self._sockets:

            socket.send(str(self._bi))
            x+=int(socket.recv())
        print(f"subroutine_3 for {self._name} is {x}")
        if x < (len(self.other_bi)+1)/3:
            self._bi=0
        elif x> (2*len(self.other_bi)+1)/3:
            return 1
    def start_routine(self):
        print(f"start_routine for {self._name} with bi={self._bi}")
        while True:
            self.subroutine_1()
            if self.subroutine_2()==0:
                self.result=0
                break
            elif self.subroutine_3()==1:
                self.result=1
                break
            
    def quantumObliviousCoinFlip(self):
        prova=[]
        for i in range(len(self._epr_socket)+1):
            prova.append(Qubit())
        return randint(0,1) #QOCC