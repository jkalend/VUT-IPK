import os
import socket


def simple_solve_plus_one_message(server_tcp, ipkcpc_tcp):
    outs = ""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as a:
        a.connect(("127.0.0.1", 2023))
        a.send(b"HELLO\nSOLVE (+ 1 2)\nBYE\n")
        for _ in range(3):
            outs += a.recv(1024).decode("utf-8")
    return outs


def invalid_query(server_tcp, ipkcpc_tcp):
    outs = ""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as a:
        a.connect(("127.0.0.1", 2023))
        a.send(b"HELLO\nSOLVE (+ a b)\nBYE\n")
        for _ in range(2):
            outs += a.recv(1024).decode("utf-8")
    return outs


def test_simple_solve_plus_one_message(server_tcp, ipkcpc_tcp):
    outs = simple_solve_plus_one_message(server_tcp, ipkcpc_tcp)
    assert outs == "HELLO\nRESULT 3\nBYE\n"


def test_invalid_query(server_tcp, ipkcpc_tcp):
    outs = invalid_query(server_tcp, ipkcpc_tcp)
    assert outs == "HELLO\nBYE\n"
