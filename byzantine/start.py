
# Python program to create the duplicate of
# an already existing file
import shutil
import os
import yaml

n = 6
print(n/3)
print((2*n)/3)
import os, glob
for filename in glob.glob("app_*"):
    os.remove(filename)
for filename in glob.glob("*.yaml"):
    os.remove(filename)
for i in range(n):
    max_qubit=2*n-1
    connections=f'''
    eprlist.append(EPRSocket("0"))
    for other in range({n}):
        if other != {i}:
            socketlist.append(Socket("{i}", str(other), log_config=app_config.log_config))'''
            
    if i == 0:
        max_qubit=2*n-1
        connections=f'''
    for other in range({n}):
        if other != {i}:
            eprlist.append(EPRSocket(str(other)))
            socketlist.append(Socket("{i}", str(other), log_config=app_config.log_config))'''
        
    
    with open(f'app_{i}.py', 'w') as f:
        f.write(f'''from netqasm.sdk.external import NetQASMConnection, Socket
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
    {connections} 
    k=2 
    alice = NetQASMConnection(
        "{i}",
        log_config=app_config.log_config,
        epr_sockets=eprlist,
        max_qubit={max_qubit},
        
        
    )
    routine = Routine(socketlist,alice, eprlist,str({i}))
    with alice:
        routine.start_routine()
    print("{i}'s result is: ", routine.result)

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
        """ print(f"subroutine_1 for {i}") """
        x=0
        x+=self._bi
        for socket in self._sockets:
            
            socket.send(str(self._bi))
            other_bi=int(socket.recv())
            self.other_bi.append(other_bi)
            x+=int(other_bi)
        print(f"subroutine_1 for {i} is " + str(x))
        if x < (len(self.other_bi)+1)/3:
            """ print(f'a {i}') """
            self._bi=0
        elif x> (2*len(self.other_bi)+1)/3:
            """ print(f'b {i}') """
            self._bi=1
        else:
            print(f'start QOCC for {i}')
            self._bi= self.quantumCoin() #QOCC
    def subroutine_2(self):
        #print(f"subroutine_2 for {i}")
        x=0
        x+=self._bi
        self.other_bi = []
        for socket in self._sockets:

            socket.send(str(self._bi))
            other_bi=int(socket.recv())
            self.other_bi.append(other_bi)
            x+=int(other_bi)
        if x < (len(self.other_bi)+1)/3:
            """ print(f"c {i}") """
            return 0
        elif x> (2*len(self.other_bi)+1)/3:
            """ print(f"d {i}") """
            self._bi=1
        
    def subroutine_3(self):
        """ print(f"subroutine_3 for {i}") """
        x=0
        self.other_bi = []
        x+=self._bi
        for socket in self._sockets:

            socket.send(str(self._bi))
            other_bi=int(socket.recv())
            self.other_bi.append(other_bi)
            x+=int(other_bi)
        print(f"subroutine_3 for {i} is " + str(x))
        if x < (len(self.other_bi)+1)/3:
            self._bi=0
        elif x> (2*len(self.other_bi)+1)/3:
            return 1
    def start_routine(self):
        print(f"start_routine for {i} with bi= "+ str(self._bi))
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
                print(f'{i} bbbbb')
                e=epr.create_keep()[0]
                print(f'{i} epr created')
                ghz[i].cnot(e)
                print(f'{i} cnot')
                ghz[i].H()
                print(f'{i} h')
                
                m1=ghz[i].measure()
                print(f'{i} m1 measured')
                
                m2=e.measure()
                print(f'{i} m2 measured')
                self._conn.flush()
                print(f'{i} flushed')
                print(f'{i} m1 ' + str(m1))
                print(f'{i} m2 ' + str(m2))
                m1,m2 = int(m1),int(m2)
                self._sockets[i].send_structured(StructuredMessage("Corrections", (m1, m2)))  # type: ignore
                print(f'sent corrections')
            m= qubit0.measure()
            self._conn.flush()
            return int(m) # type: ignore
        else:
            print(f"{i} wait for epr from leader")
            epr=self._epr_socket[leader].recv_keep()[0]
            print(f"{i} received epr from leader")
            
            print(f"{i} wait for corrections from leader")
            m1, m2 = self._sockets[leader].recv_structured().payload
            print(f"{i} received corrections from leader")
            if m2 == 1:
                epr.X()
            if m1 == 1:
                epr.Z()
            m= epr.measure()
            self._conn.flush()
            return int(m) # type: ignore
                
                
                
                
            
        prova=[]        


    ''')
os.system('''netqasm init''')
with open('network.yaml', 'r') as file:
    yamlnetwork= yaml.safe_load(file)
yamlnetwork['nodes']=[]
for i in range(n):
    if i ==0:
        qubits=[]
        for j in range(2*n-1):
            qubits.append({'id':j,'t1':0,'t2':0})
        yamlnetwork['nodes'].append({'name':str(i),'gate_fidelity':1.0, 'qubits':qubits})
    else:
        yamlnetwork['nodes'].append({'name':str(i),'gate_fidelity':1.0, 'qubits':[{'id':0,'t1':0,'t2':0},{'id':1,'t1':0,'t2':0},{'id':2,'t1':0,'t2':0}]})
with open('network.yaml', 'w') as file:
    yaml.dump(yamlnetwork, file)
    
os.system('''netqasm simulate''')
    
