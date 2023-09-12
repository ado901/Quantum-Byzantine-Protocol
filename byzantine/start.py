
# Python program to create the duplicate of
# an already existing file
import shutil
import os

# src contains the path of the source file
src_alice = r"app_alice.py"
src_bob = r"app_bob.py"

n = 5
print(n/3)
print((2*n)/3)
import os, glob
for filename in glob.glob("byzantine/app_*"):
    os.remove(filename)
for i in range(n):

    # dest contains the path of the destination file
    
    with open(f'byzantine/app_{i}.py', 'w') as f:
        f.write(f'''from netqasm.sdk.external import NetQASMConnection, Socket
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
    for other in range({n}):
        if other != {i}:
            eprlist.append(EPRSocket(str(other)))
            socketlist.append(Socket("{i}", str(other), log_config=app_config.log_config)) 
    k=2

    alice = NetQASMConnection(
        "{i}",
        log_config=app_config.log_config,
        epr_sockets=eprlist,
    )
    bi= randint(0,1)
    routine = Routine(socketlist,alice, eprlist,bi,str({i}))
    with alice:
        routine.start_routine()
    print("{i}'s result is: ", routine.result)

        


    ''')
os.system('''cd byzantine
          netqasm simulate''')
    
