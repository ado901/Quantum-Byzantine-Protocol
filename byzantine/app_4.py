from netqasm.sdk.external import NetQASMConnection, Socket
from netqasm.sdk import EPRSocket, build_types, Qubit
from netqasm.sdk.classical_communication.message import StructuredMessage
from random import randint
# setub fast byzantine agreement
def main(app_config=None):
    assert app_config is not None
    bitot=[]
    socketlist=[]
    eprlist=[]
    # Specify an EPR socket to bob
    
    eprlist.append(EPRSocket("0"))
    for other in range(6):
        if other != 4:
            socketlist.append(Socket("4", str(other), log_config=app_config.log_config)) 
    k=2 
    alice = NetQASMConnection(
        "4",
        log_config=app_config.log_config,
        epr_sockets=eprlist,
        max_qubit=11,
        
        
    )
    routine = Routine(socketlist,alice, eprlist,str(4))
    with alice:
        routine.start_routine()
    print("4's result is: ", routine.result)

class Routine:
    def __init__(self, socket: list[Socket],conn, epr_socket: list[EPRSocket], name:str):
        self._name= name
        self._sockets = socket
        self._epr_socket = epr_socket
        self._bi = int(name)%2
        self.other_bi = []
        self.result=-1
        self._conn=conn
        k=2
    
    def subroutine_1(self):
        """ print(f"subroutine_1 for 4") """
        x=0
        x+=self._bi
        for socket in self._sockets:
            
            socket.send(str(self._bi))
            other_bi=int(socket.recv())
            self.other_bi.append(other_bi)
            x+=int(other_bi)
        print(f"subroutine_1 for 4 is " + str(x))
        if x < (len(self.other_bi)+1)/3:
            """ print(f'a 4') """
            self._bi=0
        elif x> (2*len(self.other_bi)+1)/3:
            """ print(f'b 4') """
            self._bi=1
        else:
            print(f'start QOCC for 4')
            self._bi= self.quantumCoin() #QOCC
    def subroutine_2(self):
        #print(f"subroutine_2 for 4")
        x=0
        x+=self._bi
        self.other_bi = []
        for socket in self._sockets:

            socket.send(str(self._bi))
            other_bi=int(socket.recv())
            self.other_bi.append(other_bi)
            x+=int(other_bi)
        if x < (len(self.other_bi)+1)/3:
            """ print(f"c 4") """
            return 0
        elif x> (2*len(self.other_bi)+1)/3:
            """ print(f"d 4") """
            self._bi=1
        
    def subroutine_3(self):
        """ print(f"subroutine_3 for 4") """
        x=0
        self.other_bi = []
        x+=self._bi
        for socket in self._sockets:

            socket.send(str(self._bi))
            other_bi=int(socket.recv())
            self.other_bi.append(other_bi)
            x+=int(other_bi)
        print(f"subroutine_3 for 4 is " + str(x))
        if x < (len(self.other_bi)+1)/3:
            self._bi=0
        elif x> (2*len(self.other_bi)+1)/3:
            return 1
    def start_routine(self):
        print(f"start_routine for 4 with bi= "+ str(self._bi))
        while True:
            self.subroutine_1()
            if self.subroutine_2()==0:
                self.result=0
                break
            elif self.subroutine_3()==1:
                self.result=1
                break
            
    def quantumCoin(self):
        leader=0
        if int(self._name)==leader:
            
            qubit0=Qubit(self._conn)
            qubit0.H()
            ghz=[]
            ghz.append(qubit0)
            for i in range(0 ,len(self._epr_socket)): # genero GHZ
                qubit=Qubit(self._conn)
                ghz[i].cnot(qubit)
                ghz.append(qubit)
            ghz=ghz[1::] # rimuovo il primo qubit che dovrà misurare il leader
            for i,epr in enumerate(self._epr_socket): # comincio il teleport per mandare i qubit ai vari nodi
                print(f'4 bbbbb')
                e=epr.create_keep()[0]
                print(f'4 epr created')
                ghz[i].cnot(e)
                print(f'4 cnot')
                ghz[i].H()
                print(f'4 h')
                
                m1=ghz[i].measure()
                print(f'4 m1 measured')
                
                m2=e.measure()
                print(f'4 m2 measured')
                self._conn.flush()
                print(f'4 flushed')
                print(f'4 m1 ' + str(m1))
                print(f'4 m2 ' + str(m2))
                m1,m2 = int(m1),int(m2)
                self._sockets[i].send_structured(StructuredMessage("Corrections", (m1, m2)))  # type: ignore
                print(f'sent corrections')
            m= qubit0.measure()
            self._conn.flush()
            return int(m) # type: ignore
        else:
            print(f"4 wait for epr from leader")
            epr=self._epr_socket[leader].recv_keep()[0]
            print(f"4 received epr from leader")
            
            print(f"4 wait for corrections from leader")
            m1, m2 = self._sockets[leader].recv_structured().payload
            print(f"4 received corrections from leader")
            if m2 == 1:
                epr.X()
            if m1 == 1:
                epr.Z()
            m= epr.measure()
            self._conn.flush()
            return int(m) # type: ignore
                
                
                
                
            
        prova=[]        


    