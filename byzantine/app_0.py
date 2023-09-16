from netqasm.sdk.external import NetQASMConnection, Socket
from netqasm.sdk import EPRSocket, build_types, Qubit
from netqasm.sdk.classical_communication.message import StructuredMessage
from random import randint
# setub fast byzantine agreement
def main(app_config=None):
    assert app_config is not None
    eprlist:list[EPRSocket]=[]
    socketlist: list[Socket]=[]
    name="0"
    
    for i in range(5):
        if i!=0:
            eprlist.append(EPRSocket(str(i)))
            socketlist.append(Socket(name, str(i), log_config=app_config.log_config)) 
    conn=NetQASMConnection(
        app_name=app_config.app_name,
        log_config=app_config.log_config,
        epr_sockets=eprlist,
        max_qubits=10,)
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
        print(f"subroutine_1 for 0 is " + str(x))
        if x < (len(other_bi)+1)/3:
            bi=0
        elif x> (2*(len(other_bi)+1))/3:
            bi=1
        else:
            
            
            print(f'start QOCC for 0')
            with conn:
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
                    print(f'created epr with {socketlist[i].remote_app_name}')
                    count+=1
                    qlist[i].cnot(e)
                    print(f'cnoted epr of {socketlist[i].remote_app_name}')
                    qlist[i].H()
                    print(f'H to {socketlist[i].remote_app_name}')
                    m1=qlist[i].measure()
                    print(f'measured m1')
                    conn.flush()
                    m2=e.measure()
                    print(f'measured m2')
                    conn.flush()
                    m1,m2= int(m1), int(m2)
                    socketlist[i].send_structured(StructuredMessage("Corrections", (m1, m2))) # type: ignore
                    print(f"sent {m1} and {m2} to {socketlist[i].remote_app_name}")
                m=q0.measure()
                conn.flush()
                print(f'count is {count}')
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
        print(f"subroutine_3 for 0 is " + str(x))
        if x < (len(other_bi)+1)/3:
            bi=0
        elif x> (2*(len(other_bi)+1))/3:
            print(f'0s result is 1')
            break