import subprocess
import os


def termination_tcp(server_tcp):
    if os.name == "nt":
        server_tcp.send_signal(subprocess.signal.CTRL_C_EVENT)
    else:
        server_tcp.send_signal(subprocess.signal.SIGINT)
    server_tcp.wait(5)
    return server_tcp.returncode


def termination_udp(server_udp):
    if os.name == "nt":
        server_udp.send_signal(subprocess.signal.CTRL_C_EVENT)
    else:
        server_udp.send_signal(subprocess.signal.SIGINT)
    server_udp.wait(5)
    return server_udp.returncode


def test_termination_tcp(server_tcp):
    if os.name == "nt":
        assert termination_tcp(server_tcp) != 0
    else:
        assert termination_tcp(server_tcp) == -2  # -2 for SIGINT


def test_termination_udp(server_udp):
    if os.name == "nt":
        assert termination_udp(server_udp) != 0
    else:
        assert termination_udp(server_udp) == -2  # -2 for SIGINT
