from netqasm.sdk.external import NetQASMConnection, Socket
from netqasm.sdk import EPRSocket
from random import randint
from subroutines import Routine

def main(app_config=None):
    bitot=[]
    socketlist=[]
    eprlist=[]
    assert app_config is not None
    # Setup a classical socket to alice
    socketlist.append(Socket("bob", "alice", log_config=app_config.log_config))

    # Specify an EPR socket to bob
    eprlist.append(EPRSocket("alice"))

    bob = NetQASMConnection(
        "bob",
        log_config=app_config.log_config,
        epr_sockets=eprlist,
    )
    bi= 0
    routine=Routine(socketlist, eprlist,bi)
    routine.start_routine()
    print("Bob's result is: ", routine.result)


