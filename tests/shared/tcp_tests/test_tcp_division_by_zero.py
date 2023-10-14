import os


def complex_expression_with_divide_by_zero(server_tcp, ipkcpc_tcp):
    outs, errors = ipkcpc_tcp.communicate(input=b"HELLO\nSOLVE (+ 1 (* 2 (+ 3 4)) (* 5 6) (/ 7 0))\nBYE\n", timeout=3)
    return ipkcpc_tcp.returncode, outs, errors


def test_complex_expression_with_divide_by_zero(server_tcp, ipkcpc_tcp):
    ret, outs, errors = complex_expression_with_divide_by_zero(server_tcp, ipkcpc_tcp)
    assert ret == 1
    if os.name == "nt":
        assert outs == b"HELLO\r\nBYE\r\n"
    else:
        assert outs == b"HELLO\nBYE\n"
    assert errors != b""
