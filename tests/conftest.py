import pytest
import subprocess
import os
from tests.utility import find_file

@pytest.fixture(name="server_tcp")
def fixture_server_tcp():
    process = subprocess.Popen(["cmake-build-debug/ipkcpd", "-p", "2023", "-h", "localhost", "-m", "tcp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    yield process
    process.send_signal(subprocess.signal.SIGINT)


@pytest.fixture(name="server_udp")
def fixture_server_udp():
    process = subprocess.Popen(["cmake-build-debug/ipkcpd", "-p", "2023", "-h", "localhost", "-m", "udp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    yield process
    process.send_signal(subprocess.signal.SIGINT)

@pytest.fixture(name="ipkcpc_tcp")
def fixture_ipkcpc_tcp():
    process = subprocess.Popen([find_file("ipkcpc", os.getcwd()), "-p", "2023", "-h", "localhost", "-m", "tcp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    yield process
    process.send_signal(subprocess.signal.SIGINT)
    
@pytest.fixture(name="ipkcpc_udp")
def fixture_ipkcpc_udp():
    process = subprocess.Popen([find_file("ipkcpc", os.getcwd()), "-p", "2023", "-h", "localhost", "-m", "udp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    yield process
    process.send_signal(subprocess.signal.SIGINT)
    
