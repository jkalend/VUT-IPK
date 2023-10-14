import os
import subprocess


def too_many_spaces(server_udp, ipkcpc):
    outs, errors = ipkcpc.communicate(input=b"(+ 1 2  )\n", timeout=3)
    if os.name == "nt":
        ipkcpc.send_signal(subprocess.signal.CTRL_C_EVENT)
    else:
        ipkcpc.send_signal(subprocess.signal.SIGINT)
    ipkcpc.wait(5)
    return ipkcpc.returncode, outs, errors


def too_many_spaces2(server_udp, ipkcpc):
    outs, errors = ipkcpc.communicate(input=b"( + 1 2 )\n", timeout=3)
    if os.name == "nt":
        ipkcpc.send_signal(subprocess.signal.CTRL_C_EVENT)
    else:
        ipkcpc.send_signal(subprocess.signal.SIGINT)
    ipkcpc.wait(5)
    return ipkcpc.returncode, outs, errors


def too_many_spaces3(server_udp, ipkcpc):
    outs, errors = ipkcpc.communicate(input=b" (+ 1 2 )\n", timeout=3)
    if os.name == "nt":
        ipkcpc.send_signal(subprocess.signal.CTRL_C_EVENT)
    else:
        ipkcpc.send_signal(subprocess.signal.SIGINT)
    ipkcpc.wait(5)
    return ipkcpc.returncode, outs, errors


def too_many_spaces4(server_udp, ipkcpc):
    outs, errors = ipkcpc.communicate(input=b"( + 1 2)\n", timeout=3)
    if os.name == "nt":
        ipkcpc.send_signal(subprocess.signal.CTRL_C_EVENT)
    else:
        ipkcpc.send_signal(subprocess.signal.SIGINT)
    ipkcpc.wait(5)
    return ipkcpc.returncode, outs, errors

def test_too_many_spaces(server_udp, ipkcpc_udp):
    ret, outs, errors = too_many_spaces(server_udp, ipkcpc_udp)
    assert ret == 0
    if os.name == 'nt':
        assert outs == b"ERR:parsing error\r\n"
    else:
        assert outs == b"ERR:parsing error\n"


def test_too_many_spaces2(server_udp, ipkcpc_udp):
    ret, outs, errors = too_many_spaces2(server_udp, ipkcpc_udp)
    assert ret == 0
    if os.name == 'nt':
        assert outs == b"ERR:parsing error\r\n"
    else:
        assert outs == b"ERR:parsing error\n"


def test_too_many_spaces3(server_udp, ipkcpc_udp):
    ret, outs, errors = too_many_spaces3(server_udp, ipkcpc_udp)
    assert ret == 0
    if os.name == 'nt':
        assert outs == b"ERR:parsing error\r\n"
    else:
        assert outs == b"ERR:parsing error\n"


def test_too_many_spaces4(server_udp, ipkcpc_udp):
    ret, outs, errors = too_many_spaces4(server_udp, ipkcpc_udp)
    assert ret == 0
    if os.name == 'nt':
        assert outs == b"ERR:parsing error\r\n"
    else:
        assert outs == b"ERR:parsing error\n"
