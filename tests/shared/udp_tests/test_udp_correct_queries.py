import os
import subprocess

def simple_solve_plus(server_udp, ipkcpc):
    outs, errors = ipkcpc.communicate(input=b"(+ 1 2)\n", timeout=3)
    if os.name == "nt":
        ipkcpc.send_signal(subprocess.signal.CTRL_C_EVENT)
    else:
        ipkcpc.send_signal(subprocess.signal.SIGINT)
    ipkcpc.wait(5)
    return ipkcpc.returncode, outs, errors


def simple_solve_minus(server_udp, ipkcpc):
    outs, errors = ipkcpc.communicate(input=b"(- 1 2)\n", timeout=3)
    if os.name == "nt":
        ipkcpc.send_signal(subprocess.signal.CTRL_C_EVENT)
    else:
        ipkcpc.send_signal(subprocess.signal.SIGINT)
    ipkcpc.wait(5)
    return ipkcpc.returncode, outs, errors


def simple_solve_multiply(server_udp, ipkcpc):
    outs, errors = ipkcpc.communicate(input=b"(* 1 2)\n", timeout=3)
    if os.name == "nt":
        ipkcpc.send_signal(subprocess.signal.CTRL_C_EVENT)
    else:
        ipkcpc.send_signal(subprocess.signal.SIGINT)
    ipkcpc.wait(5)
    return ipkcpc.returncode, outs, errors


def simple_solve_divide(server_udp, ipkcpc):
    outs, errors = ipkcpc.communicate(input=b"(/ 1 2)\n", timeout=3)
    return ipkcpc.returncode, outs, errors


def inner_expression(server_udp, ipkcpc):
    outs, errors = ipkcpc.communicate(input=b"(+ 1 (* 2 3))\n", timeout=3)
    if os.name == "nt":
        ipkcpc.send_signal(subprocess.signal.CTRL_C_EVENT)
    else:
        ipkcpc.send_signal(subprocess.signal.SIGINT)
    ipkcpc.wait(5)
    return ipkcpc.returncode, outs, errors


def double_inner_expression(server_udp, ipkcpc):
    outs, errors = ipkcpc.communicate(input=b"(+ 1 (* 2 (+ 3 4)))\n", timeout=3)
    if os.name == "nt":
        ipkcpc.send_signal(subprocess.signal.CTRL_C_EVENT)
    else:
        ipkcpc.send_signal(subprocess.signal.SIGINT)
    ipkcpc.wait(5)
    return ipkcpc.returncode, outs, errors


def two_inner_expression(server_udp, ipkcpc):
    outs, errors = ipkcpc.communicate(input=b"(+ 1 (* 2 (+ 3 4)) (* 5 6))\n", timeout=3)
    if os.name == "nt":
        ipkcpc.send_signal(subprocess.signal.CTRL_C_EVENT)
    else:
        ipkcpc.send_signal(subprocess.signal.SIGINT)
    ipkcpc.wait(5)
    return ipkcpc.returncode, outs, errors


def complex_expression(server_udp, ipkcpc):
    outs, errors = ipkcpc.communicate(input=b"(+ 1 (* 2 (+ 3 4)) (* 5 6) (/ 7 8) (/ 1 1))\n", timeout=3)
    if os.name == "nt":
        ipkcpc.send_signal(subprocess.signal.CTRL_C_EVENT)
    else:
        ipkcpc.send_signal(subprocess.signal.SIGINT)
    ipkcpc.wait(5)
    return ipkcpc.returncode, outs, errors


def complex_expression2(server_udp, ipkcpc):
    outs, errors = ipkcpc.communicate(input=b"(+ 1 (* 45 (+ 3 4)) (* 3 6) (/ 7 8) (/ 0 1) (/ 9 100))\n", timeout=3)
    if os.name == "nt":
        ipkcpc.send_signal(subprocess.signal.CTRL_C_EVENT)
    else:
        ipkcpc.send_signal(subprocess.signal.SIGINT)
    ipkcpc.wait(5)
    return ipkcpc.returncode, outs, errors


def long_expression(server_udp, ipkcpc):
    outs, errors = ipkcpc.communicate(input=b"(+ 100 (+ 1 1) (+ 1 1) (+ 1 1) (+ 1 1) (+ 1 1) (+ 1 1) (+ 1 1) (+ 1 1) (+ 1 1) (+ 1 1) (+ 1 1))\n", timeout=3)
    if os.name == "nt":
        ipkcpc.send_signal(subprocess.signal.CTRL_C_EVENT)
    else:
        ipkcpc.send_signal(subprocess.signal.SIGINT)
    ipkcpc.wait(5)
    return ipkcpc.returncode, outs, errors


def long_expression2(server_udp, ipkcpc):
    outs, errors = ipkcpc.communicate(input=b"(* 1 1 1 1 1 1 1 1 1 1 1 0)\n", timeout=3)
    if os.name == "nt":
        ipkcpc.send_signal(subprocess.signal.CTRL_C_EVENT)
    else:
        ipkcpc.send_signal(subprocess.signal.SIGINT)
    ipkcpc.wait(5)
    return ipkcpc.returncode, outs, errors

def test_simple_solve_plus(server_udp, ipkcpc_udp):
    ret, outs, errors = simple_solve_plus(server_udp, ipkcpc_udp)
    assert ret == 0
    if os.name == 'nt':
        assert outs == b"OK:3\r\n"
    else:
        assert outs == b"OK:3\n"
    assert errors == b""


def test_simple_solve_minus(server_udp, ipkcpc_udp):
    ret, outs, errors = simple_solve_minus(server_udp, ipkcpc_udp)
    assert ret == 0
    if os.name == 'nt':
        assert outs != b""
    else:
        assert outs != b""
    assert errors == b""


def test_simple_solve_multiply(server_udp, ipkcpc_udp):
    ret, outs, errors = simple_solve_multiply(server_udp, ipkcpc_udp)
    assert ret == 0
    if os.name == 'nt':
        assert outs == b"OK:2\r\n"
    else:
        assert outs == b"OK:2\n"
    assert errors == b""


def test_simple_solve_divide(server_udp, ipkcpc_udp):
    ret, outs, errors = simple_solve_divide(server_udp, ipkcpc_udp)
    assert ret == 0
    if os.name == 'nt':
        assert outs == b"OK:0\r\n"
    else:
        assert outs == b"OK:0\n"
    assert errors == b""


def test_inner_expression(server_udp, ipkcpc_udp):
    ret, outs, errors = inner_expression(server_udp, ipkcpc_udp)
    assert ret == 0
    if os.name == 'nt':
        assert outs == b"OK:7\r\n"
    else:
        assert outs == b"OK:7\n"
    assert errors == b""


def test_double_inner_expression(server_udp, ipkcpc_udp):
    ret, outs, errors = double_inner_expression(server_udp, ipkcpc_udp)
    assert ret == 0
    if os.name == 'nt':
        assert outs == b"OK:15\r\n"
    else:
        assert outs == b"OK:15\n"
    assert errors == b""


def test_two_inner_expression(server_udp, ipkcpc_udp):
    ret, outs, errors = two_inner_expression(server_udp, ipkcpc_udp)
    assert ret == 0
    if os.name == 'nt':
        assert outs == b"OK:45\r\n"
    else:
        assert outs == b"OK:45\n"
    assert errors == b""


def test_complex_expression(server_udp, ipkcpc_udp):
    ret, outs, errors = complex_expression(server_udp, ipkcpc_udp)
    assert ret == 0
    if os.name == 'nt':
        assert outs == b"OK:46\r\n"
    else:
        assert outs == b"OK:46\n"
    assert errors == b""


def test_complex_expression2(server_udp, ipkcpc_udp):
    ret, outs, errors = complex_expression2(server_udp, ipkcpc_udp)
    assert ret == 0
    if os.name == 'nt':
        assert outs == b"OK:334\r\n"
    else:
        assert outs == b"OK:334\n"
    assert errors == b""


def test_long_expression(server_udp, ipkcpc_udp):
    ret, outs, errors = long_expression(server_udp, ipkcpc_udp)
    assert ret == 0
    if os.name == 'nt':
        assert outs == b"OK:122\r\n"
    else:
        assert outs == b"OK:122\n"
    assert errors == b""


def test_long_expression2(server_udp, ipkcpc_udp):
    ret, outs, errors = long_expression2(server_udp, ipkcpc_udp)
    assert ret == 0
    if os.name == 'nt':
        assert outs == b"OK:0\r\n"
    else:
        assert outs == b"OK:0\n"
    assert errors == b""
