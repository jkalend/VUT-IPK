import pytest
import subprocess


def termination_tcp(server_tcp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "tcp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    process.send_signal(subprocess.signal.SIGINT)
    process.wait(5)
    return process.returncode


def termination_udp(server_udp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "udp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    process.send_signal(subprocess.signal.SIGINT)
    process.wait(5)
    return process.returncode


def test_termination_tcp(server_tcp):
    assert termination_tcp(server_tcp) == -2  # -2 for SIGINT


def test_termination_udp(server_udp):
    assert termination_udp(server_udp) == -2  # -2 for SIGINT
