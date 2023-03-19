import os


def missing_handshake(server_tcp, ipkcpc_tcp):
    outs, errors = ipkcpc_tcp.communicate(input=b"SOLVE (+ 1 2)\n", timeout=10)
    return ipkcpc_tcp.returncode, outs, errors


def wrong_handshake(server_tcp, ipkcpc_tcp):
    outs, errors = ipkcpc_tcp.communicate(input=b"HELLOO\n", timeout=10)
    return ipkcpc_tcp.returncode, outs, errors


def wrong_handshake_2(server_tcp, ipkcpc_tcp):
    outs, errors = ipkcpc_tcp.communicate(input=b"HENLO\n", timeout=10)
    return ipkcpc_tcp.returncode, outs, errors


def wrong_handshake_3(server_tcp, ipkcpc_tcp):
    outs, errors = ipkcpc_tcp.communicate(input=b"H\nE\nL\nL\nO\n", timeout=10)
    return ipkcpc_tcp.returncode, outs, errors


def test_missing_handshake(server_tcp, ipkcpc_tcp):
    ret, outs, errors = missing_handshake(server_tcp, ipkcpc_tcp)
    assert ret == 1
    if os.name == "nt":
        assert outs == b"BYE\r\n"
    else:
        assert outs == b"BYE\n"
    assert errors != b""


def test_wrong_handshake(server_tcp, ipkcpc_tcp):
    ret, outs, errors = wrong_handshake(server_tcp, ipkcpc_tcp)
    assert ret == 1
    if os.name == "nt":
        assert outs == b"BYE\r\n"
    else:
        assert outs == b"BYE\n"
    assert errors != b""


def test_wrong_handshake_2(server_tcp, ipkcpc_tcp):
    ret, outs, errors = wrong_handshake_2(server_tcp, ipkcpc_tcp)
    assert ret == 1
    if os.name == "nt":
        assert outs == b"BYE\r\n"
    else:
        assert outs == b"BYE\n"
    assert errors != b""


def test_wrong_handshake_3(server_tcp, ipkcpc_tcp):
    ret, outs, errors = wrong_handshake_3(server_tcp, ipkcpc_tcp)
    assert ret == 1
    if os.name == "nt":
        assert outs == b"BYE\r\n"
    else:
        assert outs == b"BYE\n"
    assert errors != b""
