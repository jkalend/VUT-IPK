import os


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


def missing_left_bracket(server_tcp, ipkcpc_tcp):
    outs, errors = ipkcpc_tcp.communicate(input=b"HELLO\nSOLVE + 1 2)\n", timeout=3)
    return ipkcpc_tcp.returncode, outs, errors


def missing_right_bracket(server_tcp, ipkcpc_tcp):
    outs, errors = ipkcpc_tcp.communicate(input=b"HELLO\nSOLVE (+ 1 2\n", timeout=3)
    return ipkcpc_tcp.returncode, outs, errors


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
