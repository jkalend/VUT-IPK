import os


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
