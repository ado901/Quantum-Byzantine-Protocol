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
        if other != 3:
            eprlist.append(EPRSocket(str(other)))
            socketlist.append(Socket("3", str(other), log_config=app_config.log_config)) 
    k=2

    alice = NetQASMConnection(
        "3",
        log_config=app_config.log_config,
        epr_sockets=eprlist,
    )
    bi= randint(0,1)
    routine = Routine(socketlist, socketlist,bi,str(3))
    with alice:
        routine.start_routine()
    print("3's result is: ", routine.result)

        


    