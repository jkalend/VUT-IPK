import pytest
import subprocess
import select
import os
from time import sleep
from tests.utility import find_file


def correct_handshake_and_leave(server_tcp, ipkcpc_tcp):
    outs, errors = ipkcpc_tcp.communicate(input=b"HELLO\nBYE\n", timeout=3)
    return ipkcpc_tcp.returncode, outs, errors


def simple_solve_plus(server_tcp, ipkcpc_tcp):
    outs, errors = ipkcpc_tcp.communicate(input=b"HELLO\nSOLVE (+ 1 2)\nBYE\n", timeout=3)
    return ipkcpc_tcp.returncode, outs, errors


def simple_solve_minus(server_tcp, ipkcpc_tcp):
    outs, errors = ipkcpc_tcp.communicate(input=b"HELLO\nSOLVE (- 1 2)\nBYE\n", timeout=3)
    return ipkcpc_tcp.returncode, outs, errors


def simple_solve_multiply(server_tcp, ipkcpc_tcp):
    outs, errors = ipkcpc_tcp.communicate(input=b"HELLO\nSOLVE (* 1 2)\nBYE\n", timeout=3)
    return ipkcpc_tcp.returncode, outs, errors


def simple_solve_divide(server_tcp, ipkcpc_tcp):
    outs, errors = ipkcpc_tcp.communicate(input=b"HELLO\nSOLVE (/ 1 2)\nBYE\n", timeout=3)
    return ipkcpc_tcp.returncode, outs, errors


def inner_expression(server_tcp, ipkcpc_tcp):
    outs, errors = ipkcpc_tcp.communicate(input=b"HELLO\nSOLVE (+ 1 (* 2 3))\nBYE\n", timeout=3)
    return ipkcpc_tcp.returncode, outs, errors


def double_inner_expression(server_tcp, ipkcpc_tcp):
    outs, errors = ipkcpc_tcp.communicate(input=b"HELLO\nSOLVE (+ 1 (* 2 (+ 3 4)))\nBYE\n", timeout=3)
    return ipkcpc_tcp.returncode, outs, errors


def two_inner_expression(server_tcp, ipkcpc_tcp):
    outs, errors = ipkcpc_tcp.communicate(input=b"HELLO\nSOLVE (+ 1 (* 2 (+ 3 4)) (* 5 6))\nBYE\n", timeout=3)
    return ipkcpc_tcp.returncode, outs, errors


def complex_expression(server_tcp, ipkcpc_tcp):
    outs, errors = ipkcpc_tcp.communicate(input=b"HELLO\nSOLVE (+ 1 (* 2 (+ 3 4)) (* 5 6) (/ 7 8) (/ 1 1))\nBYE\n", timeout=3)
    return ipkcpc_tcp.returncode, outs, errors


def complex_expression2(server_tcp, ipkcpc_tcp):
    outs, errors = ipkcpc_tcp.communicate(input=b"HELLO\nSOLVE (+ 1 (* 45 (+ 3 4)) (* 3 6) (/ 7 8) (/ 0 1) (/ 9 100))\nBYE\n", timeout=3)
    return ipkcpc_tcp.returncode, outs, errors


def long_expression(server_tcp, ipkcpc_tcp):
    outs, errors = ipkcpc_tcp.communicate(input=b"HELLO\nSOLVE (+ 100 (+ 1 1) (+ 1 1) (+ 1 1) (+ 1 1) (+ 1 1) (+ 1 1) (+ 1 1) (+ 1 1) (+ 1 1) (+ 1 1) (+ 1 1))\nBYE\n", timeout=3)
    return ipkcpc_tcp.returncode, outs, errors


def long_expression2(server_tcp, ipkcpc_tcp):
    outs, errors = ipkcpc_tcp.communicate(input=b"HELLO\nSOLVE (* 1 1 1 1 1 1 1 1 1 1 1 0)\nBYE\n", timeout=3)
    return ipkcpc_tcp.returncode, outs, errors


def missing_expression(server_tcp, ipkcpc_tcp):
    outs, errors = ipkcpc_tcp.communicate(input=b"HELLO\nSOLVE\nBYE\n", timeout=3)
    return ipkcpc_tcp.returncode, outs, errors


def missing_solve(server_tcp, ipkcpc_tcp):
    outs, errors = ipkcpc_tcp.communicate(input=b"HELLO\n(+ 1 2)\nBYE\n", timeout=3)
    return ipkcpc_tcp.returncode, outs, errors


def too_short_expression(server_tcp, ipkcpc_tcp):
    outs, errors = ipkcpc_tcp.communicate(input=b"HELLO\nSOLVE (+ 1)\n", timeout=3)
    return ipkcpc_tcp.returncode, outs, errors


def too_short_expression2(server_tcp, ipkcpc_tcp):
    outs, errors = ipkcpc_tcp.communicate(input=b"HELLO\nSOLVE (+)\n", timeout=3)
    return ipkcpc_tcp.returncode, outs, errors


def empty_expression(server_tcp, ipkcpc_tcp):
    outs, errors = ipkcpc_tcp.communicate(input=b"HELLO\nSOLVE ()\n", timeout=3)
    return ipkcpc_tcp.returncode, outs, errors


def empty_expression2(server_tcp, ipkcpc_tcp):
    outs, errors = ipkcpc_tcp.communicate(input=b"HELLO\nSOLVE (  )\n", timeout=3)
    return ipkcpc_tcp.returncode, outs, errors


def too_many_spaces(server_tcp, ipkcpc_tcp):
    outs, errors = ipkcpc_tcp.communicate(input=b"HELLO\nSOLVE (+ 1 2  )\n", timeout=3)
    return ipkcpc_tcp.returncode, outs, errors


def too_many_spaces2(server_tcp, ipkcpc_tcp):
    outs, errors = ipkcpc_tcp.communicate(input=b"HELLO\nSOLVE ( + 1 2 )\n", timeout=3)
    return ipkcpc_tcp.returncode, outs, errors


def too_many_spaces3(server_tcp, ipkcpc_tcp):
    outs, errors = ipkcpc_tcp.communicate(input=b"HELLO\nSOLVE  (+ 1 2 )\n", timeout=3)
    return ipkcpc_tcp.returncode, outs, errors


def too_many_spaces4(server_tcp, ipkcpc_tcp):
    outs, errors = ipkcpc_tcp.communicate(input=b"HELLO\nSOLVE ( + 1 2)\n", timeout=3)
    return ipkcpc_tcp.returncode, outs, errors


def complex_expression_with_divide_by_zero(server_tcp, ipkcpc_tcp):
    outs, errors = ipkcpc_tcp.communicate(input=b"HELLO\nSOLVE (+ 1 (* 2 (+ 3 4)) (* 5 6) (/ 7 0))\nBYE\n", timeout=3)
    return ipkcpc_tcp.returncode, outs, errors


def missing_left_bracket(server_tcp, ipkcpc_tcp):
    outs, errors = ipkcpc_tcp.communicate(input=b"HELLO\nSOLVE + 1 2)\n", timeout=3)
    return ipkcpc_tcp.returncode, outs, errors


def missing_right_bracket(server_tcp, ipkcpc_tcp):
    outs, errors = ipkcpc_tcp.communicate(input=b"HELLO\nSOLVE (+ 1 2\n", timeout=3)
    return ipkcpc_tcp.returncode, outs, errors


def too_long_message(server_tcp, ipkcpc_tcp):
    outs, errors = ipkcpc_tcp.communicate(input=b"HELLO\nSOLVE (+ 1 2)\n" * 100000, timeout=3)
    ipkcpc_tcp.communicate(input=b"BYE\n", timeout=3)
    return ipkcpc_tcp.returncode, outs, errors


def no_disconnect(server, ipkcpc):
    sent = 0
    outs, errors = "", ""
    ipkcpc.stdin.write(b"HELLO\n")
    while sent != 4:
        for index, io in enumerate(select.select([ipkcpc.stdout.fileno(), ipkcpc.stderr.fileno()], [ipkcpc.stdin.fileno()], [])):
            if index == 0 and io and io[0] == ipkcpc.stdout.fileno():
                outs += ipkcpc.stdout.readline().decode("utf-8")
                sent += 1
                sleep(1)
            if index == 1 and io and io[0] == ipkcpc.stdin.fileno():
                if sent == 3:
                    ipkcpc.stdin.write(b"BYE\n")
                else:
                    ipkcpc.stdin.write(b"SOLVE (+ 1 2)\n")
            if index == 2 and io and io[0] == ipkcpc.stderr.fileno():
                errors += ipkcpc.stderr.readline().decode("utf-8")

    ipkcpc.send_signal(subprocess.signal.SIGINT)
    ipkcpc.wait(5)
    return ipkcpc.returncode, outs, errors


def many_requests(server, ipkcpc):
    sent = 0
    outs, errors = "", ""
    ipkcpc.stdin.write(b"HELLO\n")
    while sent != 101:
        for index, io in enumerate(
                select.select([ipkcpc.stdout.fileno(), ipkcpc.stderr.fileno()], [ipkcpc.stdin.fileno()], [])):
            if index == 0 and io and io[0] == ipkcpc.stdout.fileno():
                outs += ipkcpc.stdout.readline().decode("utf-8")
                sent += 1
            if index == 1 and io and io[0] == ipkcpc.stdin.fileno():
                if sent == 100:
                    ipkcpc.stdin.write(b"BYE\n")
                else:
                    ipkcpc.stdin.write(b"SOLVE (+ 1 2)\n")
            if index == 2 and io and io[0] == ipkcpc.stderr.fileno():
                errors += ipkcpc.stderr.readline().decode("utf-8")

    ipkcpc.send_signal(subprocess.signal.SIGINT)
    ipkcpc.wait(5)
    return ipkcpc.returncode, outs, errors


def many_clients():
    processes = []
    for i in range(30):
        processes.append(subprocess.Popen([find_file("ipkcpc", os.getcwd()), "-p", "2023", "-h", "localhost", "-m", "tcp"],
                                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, bufsize=0))

    for process in processes:
        process.stdin.write(b"HELLO\n")

    outs, errors = "", ""
    res = 0
    for process in processes:
        outs += process.stdout.readline().decode("utf-8")
        process.send_signal(subprocess.signal.SIGINT)
        process.wait(5)
        res += process.returncode

    return res, outs, errors


def test_correct_handshake_and_leave(server_tcp, ipkcpc_tcp):
    ret, outs, errors = correct_handshake_and_leave(server_tcp, ipkcpc_tcp)
    assert ret == 0
    if os.name == "nt":
        assert outs == b"HELLO\r\nBYE\r\n"
    else:
        assert outs == b"HELLO\nBYE\n"
    assert errors == b""


def test_simple_solve(server_tcp, ipkcpc_tcp):
    ret, outs, errors = simple_solve_plus(server_tcp, ipkcpc_tcp)
    assert ret == 0
    if os.name == "nt":
        assert outs == b"HELLO\r\nRESULT 3.000000\r\nBYE\r\n"
    else:
        assert outs == b"HELLO\nRESULT 3.000000\nBYE\n"
    assert errors == b""


def test_simple_solve_minus(server_tcp, ipkcpc_tcp):
    ret, outs, errors = simple_solve_minus(server_tcp, ipkcpc_tcp)
    assert ret == 0
    if os.name == "nt":
        assert outs == b"HELLO\r\nRESULT -1.000000\r\nBYE\r\n"
    else:
        assert outs == b"HELLO\nRESULT -1.000000\nBYE\n"
    assert errors == b""


def test_simple_solve_multiply(server_tcp, ipkcpc_tcp):
    ret, outs, errors = simple_solve_multiply(server_tcp, ipkcpc_tcp)
    assert ret == 0
    if os.name == "nt":
        assert outs == b"HELLO\r\nRESULT 2.000000\r\nBYE\r\n"
    else:
        assert outs == b"HELLO\nRESULT 2.000000\nBYE\n"
    assert errors == b""


def test_simple_solve_divide(server_tcp, ipkcpc_tcp):
    ret, outs, errors = simple_solve_divide(server_tcp, ipkcpc_tcp)
    assert ret == 0
    if os.name == "nt":
        assert outs == b"HELLO\r\nRESULT 0.500000\r\nBYE\r\n"
    else:
        assert outs == b"HELLO\nRESULT 0.500000\nBYE\n"
    assert errors == b""


def test_inner_expression(server_tcp, ipkcpc_tcp):
    ret, outs, errors = inner_expression(server_tcp, ipkcpc_tcp)
    assert ret == 0
    if os.name == "nt":
        assert outs == b"HELLO\r\nRESULT 7.000000\r\nBYE\r\n"
    else:
        assert outs == b"HELLO\nRESULT 7.000000\nBYE\n"
    assert errors == b""


def test_double_inner_expression(server_tcp, ipkcpc_tcp):
    ret, outs, errors = double_inner_expression(server_tcp, ipkcpc_tcp)
    assert ret == 0
    if os.name == "nt":
        assert outs == b"HELLO\r\nRESULT 15.000000\r\nBYE\r\n"
    else:
        assert outs == b"HELLO\nRESULT 15.000000\nBYE\n"
    assert errors == b""


def test_two_inner_expression(server_tcp, ipkcpc_tcp):
    ret, outs, errors = two_inner_expression(server_tcp, ipkcpc_tcp)
    assert ret == 0
    if os.name == "nt":
        assert outs == b"HELLO\r\nRESULT 45.000000\r\nBYE\r\n"
    else:
        assert outs == b"HELLO\nRESULT 45.000000\nBYE\n"
    assert errors == b""


def test_complex_expression(server_tcp, ipkcpc_tcp):
    ret, outs, errors = complex_expression(server_tcp, ipkcpc_tcp)
    assert ret == 0
    if os.name == "nt":
        assert outs == b"HELLO\r\nRESULT 46.875000\r\nBYE\r\n"
    else:
        assert outs == b"HELLO\nRESULT 46.875000\nBYE\n"
    assert errors == b""


def test_complex_expression2(server_tcp, ipkcpc_tcp):
    ret, outs, errors = complex_expression2(server_tcp, ipkcpc_tcp)
    assert ret == 0
    if os.name == "nt":
        assert outs == b"HELLO\r\nRESULT 334.965000\r\nBYE\r\n"
    else:
        assert outs == b"HELLO\nRESULT 334.965000\nBYE\n"
    assert errors == b""


def test_long_expression(server_tcp, ipkcpc_tcp):
    ret, outs, errors = long_expression(server_tcp, ipkcpc_tcp)
    assert ret == 0
    if os.name == "nt":
        assert outs == b"HELLO\r\nRESULT 122.000000\r\nBYE\r\n"
    else:
        assert outs == b"HELLO\nRESULT 122.000000\nBYE\n"
    assert errors == b""


def test_long_expression2(server_tcp, ipkcpc_tcp):
    ret, outs, errors = long_expression2(server_tcp, ipkcpc_tcp)
    assert ret == 0
    if os.name == "nt":
        assert outs == b"HELLO\r\nRESULT 0.000000\r\nBYE\r\n"
    else:
        assert outs == b"HELLO\nRESULT 0.000000\nBYE\n"
    assert errors == b""


def test_missing_expression(server_tcp, ipkcpc_tcp):
    ret, outs, errors = missing_expression(server_tcp, ipkcpc_tcp)
    assert ret == 1
    if os.name == "nt":
        assert outs == b"HELLO\r\nBYE\r\n"
    else:
        assert outs == b"HELLO\nBYE\n"
    assert errors != b""


def test_missing_solve(server_tcp, ipkcpc_tcp):
    ret, outs, errors = missing_solve(server_tcp, ipkcpc_tcp)
    assert ret == 1
    if os.name == "nt":
        assert outs == b"HELLO\r\nBYE\r\n"
    else:
        assert outs == b"HELLO\nBYE\n"
    assert errors != b""


def test_too_short_expression(server_tcp, ipkcpc_tcp):
    ret, outs, errors = too_short_expression(server_tcp, ipkcpc_tcp)
    assert ret == 1
    if os.name == "nt":
        assert outs == b"HELLO\r\nBYE\r\n"
    else:
        assert outs == b"HELLO\nBYE\n"
    assert errors != b""


def test_too_short_expression2(server_tcp, ipkcpc_tcp):
    ret, outs, errors = too_short_expression2(server_tcp, ipkcpc_tcp)
    assert ret == 1
    if os.name == "nt":
        assert outs == b"HELLO\r\nBYE\r\n"
    else:
        assert outs == b"HELLO\nBYE\n"
    assert errors != b""


def test_too_many_spaces(server_tcp, ipkcpc_tcp):
    ret, outs, errors = too_many_spaces(server_tcp, ipkcpc_tcp)
    assert ret == 1
    if os.name == "nt":
        assert outs == b"HELLO\r\nBYE\r\n"
    else:
        assert outs == b"HELLO\nBYE\n"
    assert errors != b""


def test_too_many_spaces2(server_tcp, ipkcpc_tcp):
    ret, outs, errors = too_many_spaces2(server_tcp, ipkcpc_tcp)
    assert ret == 1
    if os.name == "nt":
        assert outs == b"HELLO\r\nBYE\r\n"
    else:
        assert outs == b"HELLO\nBYE\n"
    assert errors != b""


def test_too_many_spaces3(server_tcp, ipkcpc_tcp):
    ret, outs, errors = too_many_spaces3(server_tcp, ipkcpc_tcp)
    assert ret == 1
    if os.name == "nt":
        assert outs == b"HELLO\r\nBYE\r\n"
    else:
        assert outs == b"HELLO\nBYE\n"
    assert errors != b""


def test_too_many_spaces4(server_tcp, ipkcpc_tcp):
    ret, outs, errors = too_many_spaces4(server_tcp, ipkcpc_tcp)
    assert ret == 1
    if os.name == "nt":
        assert outs == b"HELLO\r\nBYE\r\n"
    else:
        assert outs == b"HELLO\nBYE\n"
    assert errors != b""


def test_complex_expression_with_divide_by_zero(server_tcp, ipkcpc_tcp):
    ret, outs, errors = complex_expression_with_divide_by_zero(server_tcp, ipkcpc_tcp)
    assert ret == 1
    if os.name == "nt":
        assert outs == b"HELLO\r\nBYE\r\n"
    else:
        assert outs == b"HELLO\nBYE\n"
    assert errors != b""


def test_missing_left_bracket(server_tcp, ipkcpc_tcp):
    ret, outs, errors = missing_left_bracket(server_tcp, ipkcpc_tcp)
    assert ret == 1
    if os.name == "nt":
        assert outs == b"HELLO\r\nBYE\r\n"
    else:
        assert outs == b"HELLO\nBYE\n"
    assert errors != b""


def test_missing_right_bracket(server_tcp, ipkcpc_tcp):
    ret, outs, errors = missing_right_bracket(server_tcp, ipkcpc_tcp)
    assert ret == 1
    if os.name == "nt":
        assert outs == b"HELLO\r\nBYE\r\n"
    else:
        assert outs == b"HELLO\nBYE\n"
    assert errors != b""


def too_long_message(server_tcp, ipkcpc_tcp):
    ret, outs, errors = too_long_message(server_tcp, ipkcpc_tcp)
    assert ret == 0
    if os.name == "nt":
        assert outs == b"HELLO\r\nBYE\r\n"
    else:
        assert outs == b"HELLO\nBYE\n"
    assert errors != b""

@pytest.mark.skipif(os.name == 'nt', reason="not supported on windows")
def test_no_disconnect(server_tcp, ipkcpc_tcp):
    ret, outs, errors = no_disconnect(server_tcp, ipkcpc_tcp)
    assert ret == 0
    assert outs == "HELLO\n" + "RESULT 3.000000\n" * 3
    assert errors == ""

@pytest.mark.skipif(os.name == 'nt', reason="not supported on windows")
def test_many_requests(server_tcp, ipkcpc_tcp):
    ret, outs, errors = many_requests(server_tcp, ipkcpc_tcp)
    assert ret == 0
    assert outs == "HELLO\n" + "RESULT 3.000000\n" * 100
    assert errors == ""

@pytest.mark.skipif(os.name == 'nt', reason="not supported on windows")
def test_many_clients(server_tcp, ipkcpc_tcp):
    ret, outs, errors = many_clients()
    assert ret == 0
    assert outs == "HELLO\n" * 30
    assert errors == ""
