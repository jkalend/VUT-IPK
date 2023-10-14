import os


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


def test_simple_solve(server_tcp, ipkcpc_tcp):
    ret, outs, errors = simple_solve_plus(server_tcp, ipkcpc_tcp)
    assert ret == 0
    if os.name == "nt":
        assert outs == b"HELLO\r\nRESULT 3\r\nBYE\r\n"
    else:
        assert outs == b"HELLO\nRESULT 3\nBYE\n"
    assert errors == b""


def test_simple_solve_minus(server_tcp, ipkcpc_tcp):
    ret, outs, errors = simple_solve_minus(server_tcp, ipkcpc_tcp)
    assert ret == 1
    if os.name == "nt":
        assert outs != b""
    else:
        assert outs != b""


def test_simple_solve_multiply(server_tcp, ipkcpc_tcp):
    ret, outs, errors = simple_solve_multiply(server_tcp, ipkcpc_tcp)
    assert ret == 0
    if os.name == "nt":
        assert outs == b"HELLO\r\nRESULT 2\r\nBYE\r\n"
    else:
        assert outs == b"HELLO\nRESULT 2\nBYE\n"
    assert errors == b""


def test_simple_solve_divide(server_tcp, ipkcpc_tcp):
    ret, outs, errors = simple_solve_divide(server_tcp, ipkcpc_tcp)
    assert ret == 0
    if os.name == "nt":
        assert outs == b"HELLO\r\nRESULT 0\r\nBYE\r\n"
    else:
        assert outs == b"HELLO\nRESULT 0\nBYE\n"
    assert errors == b""


def test_inner_expression(server_tcp, ipkcpc_tcp):
    ret, outs, errors = inner_expression(server_tcp, ipkcpc_tcp)
    assert ret == 0
    if os.name == "nt":
        assert outs == b"HELLO\r\nRESULT 7\r\nBYE\r\n"
    else:
        assert outs == b"HELLO\nRESULT 7\nBYE\n"
    assert errors == b""


def test_double_inner_expression(server_tcp, ipkcpc_tcp):
    ret, outs, errors = double_inner_expression(server_tcp, ipkcpc_tcp)
    assert ret == 0
    if os.name == "nt":
        assert outs == b"HELLO\r\nRESULT 15\r\nBYE\r\n"
    else:
        assert outs == b"HELLO\nRESULT 15\nBYE\n"
    assert errors == b""


def test_two_inner_expression(server_tcp, ipkcpc_tcp):
    ret, outs, errors = two_inner_expression(server_tcp, ipkcpc_tcp)
    assert ret == 0
    if os.name == "nt":
        assert outs == b"HELLO\r\nRESULT 45\r\nBYE\r\n"
    else:
        assert outs == b"HELLO\nRESULT 45\nBYE\n"
    assert errors == b""


def test_complex_expression(server_tcp, ipkcpc_tcp):
    ret, outs, errors = complex_expression(server_tcp, ipkcpc_tcp)
    assert ret == 0
    if os.name == "nt":
        assert outs == b"HELLO\r\nRESULT 46\r\nBYE\r\n"
    else:
        assert outs == b"HELLO\nRESULT 46\nBYE\n"
    assert errors == b""


def test_complex_expression2(server_tcp, ipkcpc_tcp):
    ret, outs, errors = complex_expression2(server_tcp, ipkcpc_tcp)
    assert ret == 0
    if os.name == "nt":
        assert outs == b"HELLO\r\nRESULT 334\r\nBYE\r\n"
    else:
        assert outs == b"HELLO\nRESULT 334\nBYE\n"
    assert errors == b""


def test_long_expression(server_tcp, ipkcpc_tcp):
    ret, outs, errors = long_expression(server_tcp, ipkcpc_tcp)
    assert ret == 0
    if os.name == "nt":
        assert outs == b"HELLO\r\nRESULT 122\r\nBYE\r\n"
    else:
        assert outs == b"HELLO\nRESULT 122\nBYE\n"
    assert errors == b""


def test_long_expression2(server_tcp, ipkcpc_tcp):
    ret, outs, errors = long_expression2(server_tcp, ipkcpc_tcp)
    assert ret == 0
    if os.name == "nt":
        assert outs == b"HELLO\r\nRESULT 0\r\nBYE\r\n"
    else:
        assert outs == b"HELLO\nRESULT 0\nBYE\n"
    assert errors == b""
