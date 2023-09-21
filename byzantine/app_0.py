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
    links= yamlnetwork["links"]
    nodes=yamlnetwork['nodes']
    nodesetting=None
    for node in nodes:
        if node['name']==str(0):
            nodesetting=node
            break
    eprlist:list[EPRSocket]=[]
    socketlist: list[Socket]=[]
    name="0"
    qubitsnetwork=[]
    
    for i in range(5): # qui invece l'eprsocket va fatto con tutti gli altri nodi
        if i!=0:
            eprlist.append(EPRSocket(str(i)))
            socketlist.append(Socket(name, str(i), log_config=app_config.log_config)) 
    conn=NetQASMConnection(
        app_name=app_config.app_name,
        log_config=app_config.log_config,
        epr_sockets=eprlist,
        max_qubits=10,)
    l=0
    while (True):
        print(f'iteration {l} for node 0')
        #routine 1
        x=0
        bi=int(name)%2
        x+=bi
        other_bi = []
        for socket in socketlist:
            socket.send(str(bi))
            other_bi.append(int(socket.recv()))
            x+=int(other_bi[-1])
        print(f"subroutine_1 for 0 is " + str(x))
        if x < (len(other_bi)+1)/3:
            bi=0
        elif x> (2*(len(other_bi)+1))/3:
            bi=1
        else:
            
            
            print(f'start QC for 0')
            #grande differenza rispetto agli altri: genera stato ghz e lo distribuisce con teleport
            q0=Qubit(conn)
            q0.H()
            qlist=[q0]
            for i in range(0 ,len(eprlist)): # genero GHZ
                q=Qubit(conn)
                qlist[i].cnot(q)
                qlist.append(q)
            qlist=qlist[1::]
            for i, epr in enumerate(eprlist): #teleport
                e=epr.create_keep()[0]
                print(f'0 created epr with {socketlist[i].remote_app_name}')
                qlist[i].cnot(e)
                print(f'0 cnoted epr of {socketlist[i].remote_app_name}')
                qlist[i].H()
                print(f'0 used H to {socketlist[i].remote_app_name}')
                m1=qlist[i].measure()
                print(f'0 measured m1')
                conn.flush()
                m2=e.measure()
                print(f'0 measured m2')
                conn.flush()
                m1,m2= int(m1), int(m2)
                qubitsnetwork.append({socketlist[i].remote_app_name: {'ghz':m1, 'epr':m2}})
                socketlist[i].send_structured(StructuredMessage("Corrections", (m1, m2))) # type: ignore
                print(f"0 sent {m1} and {m2} to {socketlist[i].remote_app_name}")
            m=q0.measure()
            conn.flush()
            bi=int(m)
            
        
        # routine 2
        x=0
        x+=bi
        other_bi = []
        for socket in socketlist:
            socket.send(str(bi))
            other_bi.append(int(socket.recv()))
            x+=int(other_bi[-1])
        print(f"subroutine_2 for 0 is " + str(x))
        if x < (len(other_bi)+1)/3:
            print(f'0s result is 0')
            return {
                "result": 0,
                'qubitsnetwork': qubitsnetwork,
                'iteration': l+1
            }
        elif x> (2*(len(other_bi)+1))/3:
            bi=1
        
        
        # routine 3
        x=0
        x+=bi
        other_bi = []
        for socket in socketlist:
            socket.send(str(bi))
            other_bi.append(int(socket.recv()))
            x+=int(other_bi[-1])
        print(f"subroutine_3 for 0 is " + str(x))
        if x < (len(other_bi)+1)/3:
            bi=0
        elif x> (2*(len(other_bi)+1))/3:
            print(f'0s result is 1')
            return {
                "result": 1,
                'qubitsnetwork': qubitsnetwork,
                'iteration': l+1,
                'links': links,
                'node_setting': nodesetting
            }
        l+=1