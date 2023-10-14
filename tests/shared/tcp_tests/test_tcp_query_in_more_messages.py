import socket


def simple_solve_plus_multiple_messages(server_tcp, ipkcpc_tcp):
    outs = ""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(("127.0.0.1", 2023))
        sock.sendall(b"HELLO\n")
        sock.sendall(b"SOL")
        sock.sendall(b"VE (+ 1 2)\n")
        sock.sendall(b"BYE\n")
        for _ in range(3):
            outs += sock.recv(1024).decode("utf-8")
    return outs


def test_simple_solve_plus_multiple_messages(server_tcp, ipkcpc_tcp):
    outs = simple_solve_plus_multiple_messages(server_tcp, ipkcpc_tcp)
    assert outs == "HELLO\nRESULT 3\nBYE\n"
