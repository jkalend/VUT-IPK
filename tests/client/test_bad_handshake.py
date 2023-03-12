import subprocess
import os
from tests.utility import find_file


def missing_handshake(server_tcp):
    process = subprocess.Popen([find_file("ipkcpc", os.getcwd()), "-p", "2023", "-h", "localhost", "-m", "tcp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"SOLVE (+ 1 2)\n", timeout=10)
    return process.returncode, outs, errors


def wrong_handshake(server_tcp, ipkcpc_tcp):
    #process = subprocess.Popen([find_file("ipkcpc", os.getcwd()), "-p", "2023", "-h", "localhost", "-m", "tcp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = ipkcpc_tcp.communicate(input=b"HELLOO\n", timeout=10)
    return ipkcpc_tcp.returncode, outs, errors


def wrong_handshake_2(server_tcp):
    process = subprocess.Popen([find_file("ipkcpc", os.getcwd()), "-p", "2023", "-h", "localhost", "-m", "tcp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"HENLO\n", timeout=10)
    return process.returncode, outs, errors


def wrong_handshake_3(server_tcp):
    process = subprocess.Popen([find_file("ipkcpc", os.getcwd()), "-p", "2023", "-h", "localhost", "-m", "tcp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"H\nE\nL\nL\nO\n", timeout=10)
    return process.returncode, outs, errors


def test_missing_handshake(server_tcp):
    ret, outs, errors = missing_handshake(server_tcp)
    assert ret == 1
    assert outs == b"BYE\n"
    assert errors != b""


def test_wrong_handshake(server_tcp, ipkcpc_tcp):
    ret, outs, errors = wrong_handshake(server_tcp, ipkcpc_tcp)
    assert ret == 1
    assert outs == b"BYE\n"
    assert errors != b""


def test_wrong_handshake_2(server_tcp):
    ret, outs, errors = wrong_handshake_2(server_tcp)
    assert ret == 1
    assert outs == b"BYE\n"
    assert errors != b""
