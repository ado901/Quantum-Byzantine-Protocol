from netqasm.sdk.external import NetQASMConnection, Socket
from netqasm.sdk import EPRSocket
from random import randint
from byzantine.subroutines import Routine
# setub fast byzantine agreement
def main(app_config=None):
    assert app_config is not None
    bitot=[]
    socketlist=[]
    eprlist=[]
    # Specify an EPR socket to bob
    eprlist.append(EPRSocket("bob"))
    socketlist.append(Socket("alice", "bob", log_config=app_config.log_config)) 
    k=2

    alice = NetQASMConnection(
        "alice",
        log_config=app_config.log_config,
        epr_sockets=eprlist,
    )
    bi= 0
    routine = Routine(socketlist, socketlist,bi)
    with alice:
        routine.start_routine()
    print("Alice's result is: ", routine.result)

        


    