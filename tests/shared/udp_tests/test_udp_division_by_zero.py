import os
import subprocess


def complex_expression_with_divide_by_zero(server_udp, ipkcpc):
    outs, errors = ipkcpc.communicate(input=b"(+ 1 (* 2 (+ 3 4)) (* 5 6) (/ 7 0))\n", timeout=3)
    if os.name == "nt":
        ipkcpc.send_signal(subprocess.signal.CTRL_C_EVENT)
    else:
        ipkcpc.send_signal(subprocess.signal.SIGINT)
    ipkcpc.wait(5)
    return ipkcpc.returncode, outs, errors


def test_complex_expression_with_divide_by_zero(server_udp, ipkcpc_udp):
    ret, outs, errors = complex_expression_with_divide_by_zero(server_udp, ipkcpc_udp)
    assert ret == 0
    if os.name == 'nt':
        assert outs == b"ERR:ERROR: division by zero\r\n"
    else:
        assert outs == b"ERR:ERROR: division by zero\n"
