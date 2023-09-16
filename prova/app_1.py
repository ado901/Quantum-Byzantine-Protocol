from netqasm.logging.output import get_new_app_logger
from netqasm.runtime.settings import Simulator, get_simulator
from netqasm.sdk import EPRSocket, Qubit,build_types
from netqasm.sdk.classical_communication.message import StructuredMessage
from netqasm.sdk.external import NetQASMConnection, Socket
from netqasm.sdk.toolbox import set_qubit_state


def main(app_config=None, phi=0.0, theta=0.0):
    print(type(app_config))
    log_config = app_config.log_config
    app_logger = get_new_app_logger(app_name="sender", log_config=log_config)

    # Create a socket to send classical information
    socket = Socket("1", "0", log_config=log_config)

    # Create a EPR socket for entanglement generation
    epr_socket = EPRSocket("0")

    print("`sender` will start to teleport a qubit to `receiver`")

    # Initialize the connection to the backend
    sender = NetQASMConnection(
        app_name=app_config.app_name, log_config=log_config, epr_sockets=[epr_socket], max_qubits=8
    )
    with sender:
        # Create a qubit to teleport
        """ q = Qubit(sender) """
        """ set_qubit_state(q, phi, theta) """
        q1 = Qubit(sender)
        q2 = Qubit(sender)
        q3 = Qubit(sender)
        q4 = Qubit(sender)
        q5 = Qubit(sender)
        q6 = Qubit(sender)
        q7 = Qubit(sender)
        q8 = Qubit(sender)

        
        m1 = q1.measure()
        sender.flush()
        
        m2 = q2.measure()
        sender.flush()
        
        m3 = q3.measure()
        sender.flush()
        
        m4 = q4.measure()

        sender.flush()
        m5 = q5.measure()
        sender.flush()
        m6 = q6.measure()
        sender.flush()
        m7 = q7.measure()
        sender.flush()
        m8 = q8.measure()
        sender.flush()
        
        
        print(int(m1),int(m2),int(m3),int(m4),int(m5),int(m6),int(m7),int(m8))
        
        """ # Create EPR pairs
        epr = epr_socket.create_keep(1)

        # Teleport
        q.cnot(epr[0])
        q.H()
        m1 = q.measure()
        m2 = epr[0].measure() """

"""     # Send the correction information
    m1, m2 = int(m1), int(m2)

    app_logger.log(f"m1 = {m1}")
    app_logger.log(f"m2 = {m2}")
    print(
        f"`sender` measured the following teleportation corrections: m1 = {m1}, m2 = {m2}"
    )
    print("`sender` will send the corrections to `receiver`")

    socket.send_structured(StructuredMessage("Corrections", (m1, m2)))

    if get_simulator() == Simulator.NETSQUID:
        socket.send_silent(str((phi, theta)))

    return {"m1": m1, "m2": m2} """


if __name__ == "__main__":
    main()
