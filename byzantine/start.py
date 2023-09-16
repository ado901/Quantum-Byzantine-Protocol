
# Python program to create the duplicate of
# an already existing file
import shutil
import os
import yaml

n = 3
max_qubit=2*n
print(n/3)
print((2*n)/3)
import os, glob
for filename in glob.glob("app_*"):
    os.remove(filename)
for filename in glob.glob("*.yaml"):
    os.remove(filename)

for i in range(n):
    connection=f'''
    eprlist.append(EPRSocket("{0}")) # necessita solo di un eprsocket su 0
    for i in range({n}):
        if i!={i}:
            socketlist.append(Socket(name, str(i), log_config=app_config.log_config)) '''
    qc= f'''
            print(f'start QOCC for {i}')
            with conn: # differenza rispetto al nodo 0: riceve lo stato ghz e basta
                print(f'start QC for {i}')
                e=eprlist[0].recv_keep()[0]
                m1, m2 = socketlist[0].recv_structured().payload # type: ignore
                print(f'got {{m1}} and {{m2}} from {{socketlist[0].remote_app_name}}')
                if m2 == 1:
                    e.X()
                if m1 == 1:
                    e.Z()
                m= e.measure()
                conn.flush()
            bi=int(m)
            qubitsnetwork={{'received':{{'ghz':m1, 'epr':m2}}, 'corrected':bi}}'''
            
    if i == 0:
        qc= f'''
            
            print(f'start QOCC for {i}')
            with conn: #grande differenza rispetto agli altri: genera stato ghz e lo distribuisce con teleport
                count=0
                q0=Qubit(conn)
                count+=1
                q0.H()
                qlist=[q0]
                for i in range(0 ,len(eprlist)): # genero GHZ
                    q=Qubit(conn)
                    count+=1
                    qlist[i].cnot(q)
                    qlist.append(q)
                qlist=qlist[1::]
                for i, epr in enumerate(eprlist): #teleport
                    e=epr.create_keep()[0]
                    print(f'created epr with {{socketlist[i].remote_app_name}}')
                    count+=1
                    qlist[i].cnot(e)
                    print(f'cnoted epr of {{socketlist[i].remote_app_name}}')
                    qlist[i].H()
                    print(f'H to {{socketlist[i].remote_app_name}}')
                    m1=qlist[i].measure()
                    print(f'measured m1')
                    conn.flush()
                    m2=e.measure()
                    print(f'measured m2')
                    conn.flush()
                    m1,m2= int(m1), int(m2)
                    qubitsnetwork.append({{socketlist[i].remote_app_name: {{'ghz':m1, 'epr':m2}}}})
                    socketlist[i].send_structured(StructuredMessage("Corrections", (m1, m2))) # type: ignore
                    print(f"sent {{m1}} and {{m2}} to {{socketlist[i].remote_app_name}}")
                m=q0.measure()
                conn.flush()
                print(f'count is {{count}}')
            bi=int(m)'''
        connection=f'''
    for i in range({n}): # qui invece l'eprsocket va fatto con tutti gli altri nodi
        if i!={i}:
            eprlist.append(EPRSocket(str(i)))
            socketlist.append(Socket(name, str(i), log_config=app_config.log_config)) '''
        
    
    with open(f'app_{i}.py', 'w') as f: #GENERO I FILE PER L'APPLICAZIONE, le differenze stanno solo tra il nodo 0 (che distribuisce lo stato ghz) e gli altri
        f.write(f'''from netqasm.sdk.external import NetQASMConnection, Socket
from netqasm.sdk import EPRSocket, build_types, Qubit
from netqasm.sdk.classical_communication.message import StructuredMessage
from random import randint
# setub fast byzantine agreement
def main(app_config=None):
    assert app_config is not None
    eprlist:list[EPRSocket]=[]
    socketlist: list[Socket]=[]
    name="{i}"
    {'qubitsnetwork=[]' if i==0 else 'qubitsnetwork=None'}
    {connection}
    conn=NetQASMConnection(
        app_name=app_config.app_name,
        log_config=app_config.log_config,
        epr_sockets=eprlist,
        max_qubits={max_qubit},)
    while (True):
        #routine 1
        x=0
        bi=int(name)%2
        x+=bi
        other_bi = []
        for socket in socketlist:
            socket.send(str(bi))
            other_bi.append(int(socket.recv()))
            x+=int(other_bi[-1])
        print(f"subroutine_1 for {i} is " + str(x))
        if x < (len(other_bi)+1)/3:
            bi=0
        elif x> (2*(len(other_bi)+1))/3:
            bi=1
        else:
            {qc}
            
        
        # routine 2
        x=0
        x+=bi
        other_bi = []
        for socket in socketlist:
            socket.send(str(bi))
            other_bi.append(int(socket.recv()))
            x+=int(other_bi[-1])
        print(f"subroutine_2 for {i} is " + str(x))
        if x < (len(other_bi)+1)/3:
            print(f'{i}s result is 0')
            return {{
                "result": 0,
                'qubitsnetwork': qubitsnetwork
            }}
            break
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
        print(f"subroutine_3 for {i} is " + str(x))
        if x < (len(other_bi)+1)/3:
            bi=0
        elif x> (2*(len(other_bi)+1))/3:
            print(f'{i}s result is 1')
            return {{
                "result": 1,
                'qubitsnetwork': qubitsnetwork
            }}
            break''')
os.system('''netqasm init''')
with open('network.yaml', 'r') as file:
    yamlnetwork= yaml.safe_load(file)

nodesreplace=[]
for i, node in enumerate(yamlnetwork['nodes']): #setto i qubit (dovrebbero combaciare col parametro max_qubits) dentro lo yaml della rete
        qubits=[]
        for j in range(max_qubit):
            qubits.append({'id':j,'t1':0,'t2':0})
        nodesreplace.append({'gate_fidelity':1.0,'name':node['name'], 'qubits':qubits})
yamlnetwork['nodes']=nodesreplace
with open('network.yaml', 'w') as file:
    yaml.dump(yamlnetwork, file)
    
os.system('''netqasm simulate''')
    
