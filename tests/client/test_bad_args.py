import pytest
import subprocess

def wrong_protocol():
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "mvp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errors = process.communicate()
    return process.returncode, errors


def wrong_protocol_2():
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "123"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errors = process.communicate()
    return process.returncode, errors


def wrong_protocol_3():
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "TCP"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errors = process.communicate()
    return process.returncode, errors


def wrong_protocol_4():
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "UDP"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errors = process.communicate()
    return process.returncode, errors


def missing_protocol():
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errors = process.communicate()
    return process.returncode, errors


def wrong_host():
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localmegahost", "-m", "tcp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errors = process.communicate()
    return process.returncode, errors


def wrong_host_2():
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "1234.0.0.0", "-m", "tcp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errors = process.communicate()
    return process.returncode, errors


def wrong_host_3():
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "-1.0.0.0", "-m", "tcp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errors = process.communicate()
    return process.returncode, errors


def wrong_host_4():
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "hello.0.0.0", "-m", "tcp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errors = process.communicate()
    return process.returncode, errors


def missing_host():
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "-m", "tcp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errors = process.communicate()
    return process.returncode, errors


def wrong_port():
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "hello", "-h", "localhost", "-m", "tcp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errors = process.communicate()
    return process.returncode, errors


def wrong_port_2():
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "-1234", "-h", "localhost", "-m", "tcp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errors = process.communicate()
    return process.returncode, errors


def wrong_port_3():
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "65536000000000000000", "-h", "localhost", "-m", "tcp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errors = process.communicate()
    return process.returncode, errors


def missing_port():
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "-h", "localhost", "-m", "tcp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errors = process.communicate()
    return process.returncode, errors


def unknown_arg():
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "tcp", "-z"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errors = process.communicate()
    return process.returncode, errors


def unknown_arg_2():
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "tcp", "-z", "-y"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errors = process.communicate()
    return process.returncode, errors


def unknown_arg_3():
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "-h",  "-m", "tcp", "-tcp", "-udp", "-localhost"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errors = process.communicate()
    return process.returncode, errors


def unknown_arg_4():
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "127.0.0.1", "2023", "tcp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errors = process.communicate()
    return process.returncode, errors


def test_wrong_protocol():
    assert wrong_protocol()[0] == 1
    assert wrong_protocol()[1] == b"ERROR: invalid protocol\n"


def test_wrong_protocol_2():
    assert wrong_protocol_2()[0] == 1
    assert wrong_protocol_2()[1] == b"ERROR: invalid protocol\n"


def test_wrong_protocol_3():
    assert wrong_protocol_3()[0] == 1
    assert wrong_protocol_3()[1] == b"ERROR: invalid protocol\n"


def test_wrong_protocol_4():
    assert wrong_protocol_4()[0] == 1
    assert wrong_protocol_4()[1] == b"ERROR: invalid protocol\n"


def test_missing_protocol():
    assert missing_protocol()[0] == 1
    assert missing_protocol()[1] == b"ERROR: invalid number of arguments\n"


def test_wrong_host():
    assert wrong_host()[0] == 1
    assert wrong_host()[1] == b"ERROR: getaddrinfo failed\n"


def test_wrong_host_2():
    assert wrong_host_2()[0] == 1
    assert wrong_host_2()[1] == b"ERROR: getaddrinfo failed\n"


def test_wrong_host_3():
    assert wrong_host_3()[0] == 1
    assert wrong_host_3()[1] == b"ERROR: getaddrinfo failed\n"


def test_wrong_host_4():
    assert wrong_host_4()[0] == 1
    assert wrong_host_4()[1] == b"ERROR: getaddrinfo failed\n"


def test_missing_host():
    assert missing_host()[0] == 1
    assert missing_host()[1] == b"ERROR: invalid number of arguments\n"


def test_wrong_port():
    assert wrong_port()[0] == 1
    assert wrong_port()[1] == b"ERROR: invalid port\n"


def test_wrong_port_2():
    assert wrong_port_2()[0] == 1


def test_wrong_port_3():
    assert wrong_port_3()[0] == 1


def test_missing_port():
    assert missing_port()[0] == 1
    assert missing_port()[1] == b"ERROR: invalid number of arguments\n"


def test_unknown_arg():
    assert unknown_arg()[0] == 1
    assert unknown_arg() != b""


def test_unknown_arg_2():
    assert unknown_arg_2()[0] == 1
    assert unknown_arg_2() != b""


def test_unknown_arg_3():
    assert unknown_arg_3()[0] == 1
    assert unknown_arg_3() != b""


def test_unknown_arg_4():
    assert unknown_arg_4()[0] == 1
    assert unknown_arg_4() != b""


