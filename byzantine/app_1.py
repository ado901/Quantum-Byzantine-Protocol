from netqasm.sdk.external import NetQASMConnection, Socket
from netqasm.sdk import EPRSocket, build_types, Qubit
from netqasm.sdk.classical_communication.message import StructuredMessage
from random import randint
# setub fast byzantine agreement
def main(app_config=None):
    assert app_config is not None
    eprlist:list[EPRSocket]=[]
    socketlist: list[Socket]=[]
    name="1"
    
    eprlist.append(EPRSocket("0"))
    for i in range(5):
        if i!=1:
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
        print(f"subroutine_1 for 1 is " + str(x))
        if x < (len(other_bi)+1)/3:
            bi=0
        elif x> (2*(len(other_bi)+1))/3:
            bi=1
        else:
            
            print(f'start QOCC for 1')
            with conn:
                print(f'start QC for 1')
                e=eprlist[0].recv_keep()[0]
                m1, m2 = socketlist[0].recv_structured().payload # type: ignore
                print(f'got {m1} and {m2} from {socketlist[0].remote_app_name}')
                if m2 == 1:
                    e.X()
                if m1 == 1:
                    e.Z()
                m= e.measure()
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
        print(f"subroutine_2 for 1 is " + str(x))
        if x < (len(other_bi)+1)/3:
            print(f'1s result is 0')
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
        print(f"subroutine_3 for 1 is " + str(x))
        if x < (len(other_bi)+1)/3:
            bi=0
        elif x> (2*(len(other_bi)+1))/3:
            print(f'1s result is 1')
            break