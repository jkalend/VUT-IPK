import os
import subprocess


def missing_expression(server_udp, ipkcpc):
    outs, errors = ipkcpc.communicate(input=b"SOLVE\n", timeout=3)
    if os.name == "nt":
        ipkcpc.send_signal(subprocess.signal.CTRL_C_EVENT)
    else:
        ipkcpc.send_signal(subprocess.signal.SIGINT)
    ipkcpc.wait(5)
    return ipkcpc.returncode, outs, errors


def redundant_solve(server_udp, ipkcpc):
    outs, errors = ipkcpc.communicate(input=b"SOLVE (+ 1 2)\n", timeout=3)
    if os.name == "nt":
        ipkcpc.send_signal(subprocess.signal.CTRL_C_EVENT)
    else:
        ipkcpc.send_signal(subprocess.signal.SIGINT)
    ipkcpc.wait(5)
    return ipkcpc.returncode, outs, errors


def too_short_expression(server_udp, ipkcpc):
    outs, errors = ipkcpc.communicate(input=b"(+ 1)\n", timeout=3)
    if os.name == "nt":
        ipkcpc.send_signal(subprocess.signal.CTRL_C_EVENT)
    else:
        ipkcpc.send_signal(subprocess.signal.SIGINT)
    ipkcpc.wait(5)
    return ipkcpc.returncode, outs, errors


def too_short_expression2(server_udp, ipkcpc):
    outs, errors = ipkcpc.communicate(input=b"(+)\n", timeout=3)
    if os.name == "nt":
        ipkcpc.send_signal(subprocess.signal.CTRL_C_EVENT)
    else:
        ipkcpc.send_signal(subprocess.signal.SIGINT)
    ipkcpc.wait(5)
    return ipkcpc.returncode, outs, errors


def empty_expression(server_udp, ipkcpc):
    outs, errors = ipkcpc.communicate(input=b"()\n", timeout=3)
    if os.name == "nt":
        ipkcpc.send_signal(subprocess.signal.CTRL_C_EVENT)
    else:
        ipkcpc.send_signal(subprocess.signal.SIGINT)
    ipkcpc.wait(5)
    return ipkcpc.returncode, outs, errors


def empty_expression2(server_udp, ipkcpc):
    outs, errors = ipkcpc.communicate(input=b"(  )\n", timeout=3)
    if os.name == "nt":
        ipkcpc.send_signal(subprocess.signal.CTRL_C_EVENT)
    else:
        ipkcpc.send_signal(subprocess.signal.SIGINT)
    ipkcpc.wait(5)
    return ipkcpc.returncode, outs, errors


def missing_left_bracket(server_udp, ipkcpc):
    outs, errors = ipkcpc.communicate(input=b"+ 1 2)\n", timeout=3)
    if os.name == "nt":
        ipkcpc.send_signal(subprocess.signal.CTRL_C_EVENT)
    else:
        ipkcpc.send_signal(subprocess.signal.SIGINT)
    ipkcpc.wait(5)
    return ipkcpc.returncode, outs, errors


def missing_right_bracket(server_udp, ipkcpc):
    outs, errors = ipkcpc.communicate(input=b"(+ 1 2\n", timeout=3)
    if os.name == "nt":
        ipkcpc.send_signal(subprocess.signal.CTRL_C_EVENT)
    else:
        ipkcpc.send_signal(subprocess.signal.SIGINT)
    ipkcpc.wait(5)
    return ipkcpc.returncode, outs, errors


def test_missing_expression(server_udp, ipkcpc_udp):
    ret, outs, errors = missing_expression(server_udp, ipkcpc_udp)
    assert ret == 0
    if os.name == 'nt':
        assert outs == b"ERR:parsing error\r\n"
    else:
        assert outs == b"ERR:parsing error\n"


def test_redundant_solve(server_udp, ipkcpc_udp):
    ret, outs, errors = redundant_solve(server_udp, ipkcpc_udp)
    assert ret == 0
    if os.name == 'nt':
        assert outs == b"ERR:parsing error\r\n"
    else:
        assert outs == b"ERR:parsing error\n"


def test_too_short_expression(server_udp, ipkcpc_udp):
    ret, outs, errors = too_short_expression(server_udp, ipkcpc_udp)
    assert ret == 0
    if os.name == 'nt':
        assert outs == b"ERR:parsing error\r\n"
    else:
        assert outs == b"ERR:parsing error\n"


def test_too_short_expression2(server_udp, ipkcpc_udp):
    ret, outs, errors = too_short_expression2(server_udp, ipkcpc_udp)
    assert ret == 0
    if os.name == 'nt':
        assert outs == b"ERR:parsing error\r\n"
    else:
        assert outs == b"ERR:parsing error\n"


def test_missing_left_bracket(server_udp, ipkcpc_udp):
    ret, outs, errors = missing_left_bracket(server_udp, ipkcpc_udp)
    assert ret == 0
    if os.name == 'nt':
        assert outs == b"ERR:parsing error\r\n"
    else:
        assert outs == b"ERR:parsing error\n"


def test_missing_right_bracket(server_udp, ipkcpc_udp):
    ret, outs, errors = missing_right_bracket(server_udp, ipkcpc_udp)
    assert ret == 0
    if os.name == 'nt':
        assert outs == b"ERR:parsing error\r\n"
    else:
        assert outs == b"ERR:parsing error\n"
