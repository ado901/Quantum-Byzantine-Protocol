from netqasm.sdk.external import NetQASMConnection, Socket
from netqasm.sdk import EPRSocket
from random import randint
from subroutines import Routine
# setub fast byzantine agreement
def main(app_config=None):
    assert app_config is not None
    bitot=[]
    socketlist=[]
    eprlist=[]
    # Specify an EPR socket to bob
    for other in range(5):
        if other != 1:
            eprlist.append(EPRSocket(str(other)))
            socketlist.append(Socket("1", str(other), log_config=app_config.log_config)) 
    k=2

    alice = NetQASMConnection(
        "1",
        log_config=app_config.log_config,
        epr_sockets=eprlist,
    )
    bi= randint(0,1)
    routine = Routine(socketlist,alice, eprlist,bi,str(1))
    with alice:
        routine.start_routine()
    print("1's result is: ", routine.result)

        


    