import pytest
import subprocess
import os
from tests.utility import find_file


@pytest.fixture(name="server_tcp")
def fixture_server_tcp():
    if os.name == "nt":
        process = subprocess.Popen([find_file("ipkcpd.exe", os.getcwd()), "-p", "2023", "-h", "127.0.0.1", "-m", "tcp"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                                   creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    else:
        process = subprocess.Popen([find_file("ipkcpd", os.getcwd()), "-p", "2023", "-h", "localhost", "-m", "tcp"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    yield process
    if os.name == "nt":
        process.terminate()
    else:
        process.send_signal(subprocess.signal.SIGINT)


@pytest.fixture(name="server_udp")
def fixture_server_udp():
    if os.name == "nt":
        process = subprocess.Popen([find_file("ipkcpd.exe", os.getcwd()), "-p", "2023", "-h", "127.0.0.1", "-m", "udp"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                                   creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    else:
        process = subprocess.Popen([find_file("ipkcpd", os.getcwd()), "-p", "2023", "-h", "localhost", "-m", "udp"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    yield process
    if os.name == "nt":
        process.terminate()
    else:
        process.send_signal(subprocess.signal.SIGINT)


@pytest.fixture(name="ipkcpc_tcp")
def fixture_ipkcpc_tcp():
    if os.name == "nt":
        process = subprocess.Popen([find_file("ipkcpc.exe", os.getcwd()), "-p", "2023", "-h", "127.0.0.1", "-m", "tcp"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                                   creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    else:
        process = subprocess.Popen([find_file("ipkcpc", os.getcwd()), "-p", "2023", "-h", "localhost", "-m", "tcp"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    yield process
    if os.name == "nt":
        process.terminate()
    else:
        process.send_signal(subprocess.signal.SIGINT)


@pytest.fixture(name="ipkcpc_udp")
def fixture_ipkcpc_udp():
    if os.name == 'nt':
        process = subprocess.Popen([find_file("ipkcpc.exe", os.getcwd()), "-p", "2023", "-h", "127.0.0.1", "-m", "udp"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                                   creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    else:
        process = subprocess.Popen([find_file("ipkcpc", os.getcwd()), "-p", "2023", "-h", "localhost", "-m", "udp"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    yield process
    if os.name == "nt":
        process.terminate()
    else:
        process.send_signal(subprocess.signal.SIGINT)
