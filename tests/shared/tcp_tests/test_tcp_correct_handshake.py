import os


def correct_handshake_and_leave(server_tcp, ipkcpc_tcp):
    outs, errors = ipkcpc_tcp.communicate(input=b"HELLO\nBYE\n", timeout=3)
    return ipkcpc_tcp.returncode, outs, errors


def test_correct_handshake_and_leave(server_tcp, ipkcpc_tcp):
    ret, outs, errors = correct_handshake_and_leave(server_tcp, ipkcpc_tcp)
    assert ret == 0
    if os.name == "nt":
        assert outs == b"HELLO\r\nBYE\r\n"
    else:
        assert outs == b"HELLO\nBYE\n"
    assert errors == b""
