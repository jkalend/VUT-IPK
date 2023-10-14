import pytest
import subprocess
from time import sleep
import os
import select
import socket
from tests.utility import find_file


def too_long_message(server_udp, ipkcpc):
    outs, errors = ipkcpc.communicate(input=b"a" * 10000 + b"\n", timeout=3)
    if os.name == "nt":
        ipkcpc.send_signal(subprocess.signal.CTRL_C_EVENT)
    else:
        ipkcpc.send_signal(subprocess.signal.SIGINT)
    ipkcpc.wait(5)
    return ipkcpc.returncode, outs, errors


def continue_after_error(server_udp, ipkcpc):
    outs, errors = ipkcpc.communicate(input=b"(+ 1 2\n(+ 1 2)\n", timeout=3)
    if os.name == "nt":
        ipkcpc.send_signal(subprocess.signal.CTRL_C_EVENT)
    else:
        ipkcpc.send_signal(subprocess.signal.SIGINT)
    ipkcpc.wait(5)
    return ipkcpc.returncode, outs, errors


@pytest.mark.skipif(os.name == 'nt', reason='UNIX only')
def no_disconnect(server_udp, ipkcpc):
    sent = 0
    outs, errors = "", ""
    while sent != 3:
        for index, io in enumerate(select.select([ipkcpc.stdout.fileno(), ipkcpc.stderr.fileno()], [ipkcpc.stdin.fileno()], [])):
            if index == 0 and io and io[0] == ipkcpc.stdout.fileno():
                outs += ipkcpc.stdout.readline().decode("utf-8")
                sent += 1
                sleep(2)
            if index == 1 and io and io[0] == ipkcpc.stdin.fileno():
                ipkcpc.stdin.write(b"(+ 1 2)\n")
            if index == 2 and io and io[0] == ipkcpc.stderr.fileno():
                errors += ipkcpc.stderr.readline().decode("utf-8")

    if os.name == "nt":
        ipkcpc.send_signal(subprocess.signal.CTRL_C_EVENT)
    else:
        ipkcpc.send_signal(subprocess.signal.SIGINT)
    ipkcpc.wait(5)
    return ipkcpc.returncode, outs, errors


def many_requests(server_udp, ipkcpc):
    sent = 0
    outs, errors = "", ""
    while sent != 1000:
        for index, io in enumerate(
                select.select([ipkcpc.stdout.fileno(), ipkcpc.stderr.fileno()], [ipkcpc.stdin.fileno()], [])):
            if index == 0 and io and io[0] == ipkcpc.stdout.fileno():
                outs += ipkcpc.stdout.readline().decode("utf-8")
                sent += 1
            if index == 1 and io and io[0] == ipkcpc.stdin.fileno():
                ipkcpc.stdin.write(b"(+ 1 2)\n")
            if index == 2 and io and io[0] == ipkcpc.stderr.fileno():
                errors += ipkcpc.stderr.readline().decode("utf-8")

    if os.name == "nt":
        ipkcpc.send_signal(subprocess.signal.CTRL_C_EVENT)
    else:
        ipkcpc.send_signal(subprocess.signal.SIGINT)
    ipkcpc.wait(5)
    return ipkcpc.returncode, outs, errors


def many_clients():
    processes = []
    for i in range(30):
        processes.append(subprocess.Popen([find_file("ipkcpc", os.getcwd()), "-p", "2023", "-h", "localhost", "-m", "udp"],
                                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, bufsize=0))

    for process in processes:
        process.stdin.write(b"(+ 1 2)\n")

    outs, errors = "", ""
    res = 0
    for process in processes:
        outs += process.stdout.readline().decode("utf-8")
        process.send_signal(subprocess.signal.SIGINT)
        process.wait(5)
        res += process.returncode

    return res, outs, errors


def many_clients_many_requests(server_udp, ipkcpc):
    processes = []
    for i in range(10):
        processes.append(subprocess.Popen(["python3", find_file("udp_spammer.py", os.getcwd())], stdout=subprocess.PIPE))

    outs = ""
    sleep(2)
    for process in processes:
        process.wait(60)
        outs += process.stdout.read().decode("utf-8")

    return outs


@pytest.mark.skip(reason="not relevant for server")
def test_too_long_message(server_udp, ipkcpc_udp):
    outs = b""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as a:
        a.sendto(b"\00\77(+ 1 2)", ("127.0.0.1", 2023))
        outs = a.recvfrom(1024)
    if os.name == 'nt':
        assert outs == b"ERR:parsing error"
    else:
        assert outs == b"ERR:parsing error"


def test_continue_after_error(server_udp, ipkcpc_udp):
    ret, outs, errors = continue_after_error(server_udp, ipkcpc_udp)
    assert ret == 0
    if os.name == 'nt':
        assert outs == b"ERR:parsing error\r\nOK:3\r\n"
    else:
        assert outs == b"ERR:parsing error\nOK:3\n"


@pytest.mark.skipif(os.name == 'nt', reason="not supported on windows")
def test_no_disconnect(server_udp, ipkcpc_udp):
    res, outs, errors = no_disconnect(server_udp, ipkcpc_udp)
    assert res == 0
    assert outs == "OK:3\n" * 3
    assert errors == ""


@pytest.mark.skipif(os.name == 'nt', reason="not supported on windows")
def test_many_requests(server_udp, ipkcpc_udp):
    res, outs, errors = many_requests(server_udp, ipkcpc_udp)
    assert res == 0
    assert outs == "OK:3\n" * 1000
    assert errors == ""


@pytest.mark.skipif(os.name == 'nt', reason="not supported on windows")
def test_many_clients(server_udp, ipkcpc_udp):
    res, outs, errors = many_clients()
    assert res == 0
    assert outs == "OK:3\n" * 30
    assert errors == ""


@pytest.mark.skipif(os.name == 'nt', reason="not supported on windows")
def test_many_clients_many_requests(server_udp, ipkcpc_udp):
    outs = many_clients_many_requests(server_udp, ipkcpc_udp)
    assert outs == "OK:3\n" * 50 * 10
