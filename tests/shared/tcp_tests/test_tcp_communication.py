import pytest
import subprocess
import select
import os
from time import sleep
from tests.utility import find_file


def too_long_message(server_tcp, ipkcpc_tcp):
    message = "1 1" * 100000
    message = b"HELLO\nSOLVE (" + message.encode() + b")\nBYE\n"
    outs, errors = ipkcpc_tcp.communicate(input=message, timeout=3)
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


@pytest.mark.skipif(os.name == 'nt', reason="not supported on windows")
def test_no_disconnect(server_tcp, ipkcpc_tcp):
    ret, outs, errors = no_disconnect(server_tcp, ipkcpc_tcp)
    assert ret == 0
    assert outs == "HELLO\n" + "RESULT 3\n" * 3
    assert errors == ""

@pytest.mark.skipif(os.name == 'nt', reason="not supported on windows")
def test_many_requests(server_tcp, ipkcpc_tcp):
    ret, outs, errors = many_requests(server_tcp, ipkcpc_tcp)
    assert ret == 0
    assert outs == "HELLO\n" + "RESULT 3\n" * 100
    assert errors == ""

@pytest.mark.skipif(os.name == 'nt', reason="not supported on windows")
def test_many_clients(server_tcp, ipkcpc_tcp):
    ret, outs, errors = many_clients()
    assert ret == 0
    assert outs == "HELLO\n" * 30
    assert errors == ""
