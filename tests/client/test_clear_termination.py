import subprocess
import os


def termination_tcp(server_tcp, ipkcpc):
    if os.name == "nt":
        ipkcpc.send_signal(subprocess.signal.CTRL_C_EVENT)
    else:
        ipkcpc.send_signal(subprocess.signal.SIGINT)
    return ipkcpc.returncode


def termination_udp(server_udp, ipkcpc):
    if os.name == "nt":
        ipkcpc.send_signal(subprocess.signal.CTRL_C_EVENT)
    else:
        ipkcpc.send_signal(subprocess.signal.SIGINT)
    return ipkcpc.returncode


def test_termination_tcp(server_tcp, ipkcpc_tcp):
    assert termination_tcp(server_tcp, ipkcpc_tcp) != 0  # -2 for SIGINT


def test_termination_udp(server_udp, ipkcpc_udp):
    assert termination_udp(server_udp, ipkcpc_udp) != 0  # -2 for SIGINT
