from netqasm.runtime.settings import Simulator, get_simulator
from netqasm.sdk import EPRSocket,build_types, Qubit
from netqasm.sdk.external import NetQASMConnection, Socket, get_qubit_state
from netqasm.sdk.toolbox.sim_states import get_fidelity, qubit_from, to_dm


def main(app_config=None):
    log_config = app_config.log_config

    # Create a socket to recv classical information
    socket = Socket("0", "1", log_config=log_config)

    # Create a EPR socket for entanglement generation
    epr_socket = EPRSocket("1")

    # Initialize the connection
    receiver = NetQASMConnection(
        app_name=app_config.app_name, log_config=log_config, epr_sockets=[epr_socket],max_qubits=8
    )
    with receiver:
        q1 = Qubit(receiver)
        q2 = Qubit(receiver)
        q3 = Qubit(receiver)
        q4 = Qubit(receiver)
        q5 = Qubit(receiver)
        q6 = Qubit(receiver)
        q7 = Qubit(receiver)
        q8 = Qubit(receiver)
        
        
        m1 = q1.measure()
        receiver.flush()
        
        m2 = q2.measure()
        receiver.flush()
        
        m3 = q3.measure()
        receiver.flush()
        
        m4 = q4.measure()

        receiver.flush()
        m5 = q5.measure()
        receiver.flush()
        m6 = q6.measure()
        receiver.flush()
        m7 = q7.measure()
        receiver.flush()
        m8 = q8.measure()
        receiver.flush()
        """ epr = epr_socket.recv_keep()[0]
        receiver.flush()

        # Get the corrections
        m1, m2 = socket.recv_structured().payload
        print(f"`receiver` got corrections: {m1}, {m2}")
        if m2 == 1:
            print("`receiver` will perform X correction")
            epr.X()
        if m1 == 1:
            print("`receiver` will perform Z correction")
            epr.Z()

        receiver.flush()

        if get_simulator() == Simulator.NETSQUID:
            # Get the qubit state
            # NOTE only possible in simulation, not part of actual application
            dm = get_qubit_state(epr)
            print(f"`receiver` recieved the teleported state {dm}")

            # Reconstruct the original qubit to compare with the received one.
            # NOTE only to check simulation results, normally the Sender does not
            # need to send the phi and theta values!
            msg = socket.recv_silent()  # don't log this
            print(f"received silent message: {msg}")
            phi, theta = eval(msg)

            original = qubit_from(phi, theta)
            original_dm = to_dm(original)
            fidelity = get_fidelity(original, dm)

            return {
                "original_state": original_dm.tolist(),
                "correction1": "Z" if m1 == 1 else "None",
                "correction2": "X" if m2 == 1 else "None",
                "received_state": dm.tolist(),
                "fidelity": fidelity,
            }
        else:
            return {
                "correction1": "Z" if m1 == 1 else "None",
                "correction2": "X" if m2 == 1 else "None",
            } """


if __name__ == "__main__":
    main()
