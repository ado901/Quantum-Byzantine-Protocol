from netqasm.sdk.external import NetQASMConnection, Socket
from netqasm.sdk import EPRSocket, build_types, Qubit
from netqasm.sdk.classical_communication.message import StructuredMessage
import yaml
from random import randint
# setub fast byzantine agreement
def main(app_config=None):
    assert app_config is not None
    with open('network.yaml', 'r') as file:
        yamlnetwork= yaml.safe_load(file)
    
    nodes=yamlnetwork['nodes']
    nodesetting=None
    for node in nodes:
        if node['name']==str(2):
            nodesetting=node
            break
    eprlist:list[EPRSocket]=[]
    socketlist: list[Socket]=[]
    name="2"
    qubitsnetwork=None
    
    eprlist.append(EPRSocket("0")) # necessita solo di un eprsocket su 0
    for i in range(3):
        if i!=2:
            socketlist.append(Socket(name, str(i), log_config=app_config.log_config)) 
    conn=NetQASMConnection(
        app_name=app_config.app_name,
        log_config=app_config.log_config,
        epr_sockets=eprlist,
        max_qubits=6,)
    l=0
    while (True):
        print(f'iteration {l} for node 2')
        #routine 1
        x=0
        bi=int(name)%2
        x+=bi
        other_bi = []
        for socket in socketlist:
            socket.send(str(bi))
            other_bi.append(int(socket.recv()))
            x+=int(other_bi[-1])
        print(f"subroutine_1 for 2 is " + str(x))
        if x < (len(other_bi)+1)/3:
            bi=0
        elif x> (2*(len(other_bi)+1))/3:
            bi=1
        else:
            
            print(f'start QC for 2')
            # differenza rispetto al nodo 0: riceve lo stato ghz e basta
            e=eprlist[0].recv_keep()[0]
            m1, m2 = socketlist[0].recv_structured().payload # type: ignore
            print(f'2 got {m1} and {m2} from {socketlist[0].remote_app_name}')
            if m2 == 1:
                e.X()
            if m1 == 1:
                e.Z()
            m= e.measure()
            conn.flush()
            bi=int(m)
            qubitsnetwork={'received':{'ghz':m1, 'epr':m2}, 'corrected':bi}
            
        
        # routine 2
        x=0
        x+=bi
        other_bi = []
        for socket in socketlist:
            socket.send(str(bi))
            other_bi.append(int(socket.recv()))
            x+=int(other_bi[-1])
        print(f"subroutine_2 for 2 is " + str(x))
        if x < (len(other_bi)+1)/3:
            print(f'2s result is 0')
            return {
                "result": 0,
                'qubitsnetwork': qubitsnetwork,
                'iteration': l+1
            }
        elif x> (2*(len(other_bi)+1))/3:
            bi=1
        else:
            bi=0
        
        
        # routine 3
        x=0
        x+=bi
        other_bi = []
        for socket in socketlist:
            socket.send(str(bi))
            other_bi.append(int(socket.recv()))
            x+=int(other_bi[-1])
        print(f"subroutine_3 for 2 is " + str(x))
        if x < (len(other_bi)+1)/3:
            bi=0
        elif x> (2*(len(other_bi)+1))/3:
            print(f'2s result is 1')
            return {
                "result": 1,
                'qubitsnetwork': qubitsnetwork,
                'iteration': l+1,
                
                'node_setting': nodesetting
            }
        else:
            bi=1
        l+=1