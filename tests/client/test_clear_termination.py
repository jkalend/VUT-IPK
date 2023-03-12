import subprocess


def termination_tcp(server_tcp, ipkcpc):
    ipkcpc.send_signal(subprocess.signal.SIGINT)
    ipkcpc.wait(5)
    return ipkcpc.returncode


def termination_udp(server_udp, ipkcpc):
    ipkcpc.send_signal(subprocess.signal.SIGINT)
    ipkcpc.wait(5)
    return ipkcpc.returncode


def test_termination_tcp(server_tcp, ipkcpc_tcp):
    assert termination_tcp(server_tcp, ipkcpc_tcp) == -2  # -2 for SIGINT


def test_termination_udp(server_udp, ipkcpc_udp):
    assert termination_udp(server_udp, ipkcpc_udp) == -2  # -2 for SIGINT
