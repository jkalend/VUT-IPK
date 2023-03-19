import subprocess
import os
from tests.utility import find_file


def wrong_protocol():
    if os.name == "nt":
        process = subprocess.Popen([find_file("ipkcpc.exe", os.getcwd()), "-p", "2023", "-h", "localhost", "-m", "mvp"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        process = subprocess.Popen([find_file("ipkcpc", os.getcwd()), "-p", "2023", "-h", "localhost", "-m", "mvp"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errors = process.communicate()
    return process.returncode, errors


def wrong_protocol_2():
    if os.name == "nt":
        process = subprocess.Popen([find_file("ipkcpc.exe", os.getcwd()), "-p", "2023", "-h", "localhost", "-m", "123"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        process = subprocess.Popen([find_file("ipkcpc", os.getcwd()), "-p", "2023", "-h", "localhost", "-m", "123"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errors = process.communicate()
    return process.returncode, errors


def wrong_protocol_3():
    if os.name == "nt":
        process = subprocess.Popen([find_file("ipkcpc.exe", os.getcwd()), "-p", "2023", "-h", "localhost", "-m", "TCP"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        process = subprocess.Popen([find_file("ipkcpc", os.getcwd()), "-p", "2023", "-h", "localhost", "-m", "TCP"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errors = process.communicate()
    return process.returncode, errors


def wrong_protocol_4():
    if os.name == "nt":
        process = subprocess.Popen([find_file("ipkcpc.exe", os.getcwd()), "-p", "2023", "-h", "localhost", "-m", "UDP"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        process = subprocess.Popen([find_file("ipkcpc", os.getcwd()), "-p", "2023", "-h", "localhost", "-m", "UDP"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errors = process.communicate()
    return process.returncode, errors


def missing_protocol():
    if os.name == "nt":
        process = subprocess.Popen([find_file("ipkcpc.exe", os.getcwd()), "-p", "2023", "-h", "127.0.0.1", "-m"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        process = subprocess.Popen([find_file("ipkcpc", os.getcwd()), "-p", "2023", "-h", "localhost", "-m"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errors = process.communicate()
    return process.returncode, errors


def wrong_host():
    if os.name == "nt":
        process = subprocess.Popen([find_file("ipkcpc.exe", os.getcwd()), "-p", "2023", "-h", "localmegahost", "-m", "tcp"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        process = subprocess.Popen([find_file("ipkcpc", os.getcwd()), "-p", "2023", "-h", "localmegahost", "-m", "tcp"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errors = process.communicate()
    return process.returncode, errors


def wrong_host_2():
    if os.name == "nt":
        process = subprocess.Popen([find_file("ipkcpc.exe", os.getcwd()), "-p", "2023", "-h", "1234.0.0.0", "-m", "tcp"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        process = subprocess.Popen([find_file("ipkcpc", os.getcwd()), "-p", "2023", "-h", "1234.0.0.0", "-m", "tcp"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errors = process.communicate()
    return process.returncode, errors


def wrong_host_3():
    if os.name == "nt":
        process = subprocess.Popen([find_file("ipkcpc.exe", os.getcwd()), "-p", "2023", "-h", "-1.0.0.0", "-m", "tcp"],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        process = subprocess.Popen([find_file("ipkcpc", os.getcwd()), "-p", "2023", "-h", "-1.0.0.0", "-m", "tcp"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errors = process.communicate()
    return process.returncode, errors


def wrong_host_4():
    if os.name == "nt":
        process = subprocess.Popen([find_file("ipkcpc.exe", os.getcwd()), "-p", "2023", "-h", "hello.0.0.0", "-m", "tcp"],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        process = subprocess.Popen([find_file("ipkcpc", os.getcwd()), "-p", "2023", "-h", "hello.0.0.0", "-m", "tcp"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errors = process.communicate()
    return process.returncode, errors


def missing_host():
    if os.name == "nt":
        process = subprocess.Popen([find_file("ipkcpc.exe", os.getcwd()), "-p", "2023", "-m", "tcp"],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        process = subprocess.Popen([find_file("ipkcpc", os.getcwd()), "-p", "2023", "-h", "-m", "tcp"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errors = process.communicate()
    return process.returncode, errors


def wrong_port():
    if os.name == "nt":
        process = subprocess.Popen([find_file("ipkcpc.exe", os.getcwd()), "-p", "hello", "-h", "localhost", "-m", "tcp"],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        process = subprocess.Popen([find_file("ipkcpc", os.getcwd()), "-p", "hello", "-h", "localhost", "-m", "tcp"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errors = process.communicate()
    return process.returncode, errors


def wrong_port_2():
    if os.name == "nt":
        process = subprocess.Popen([find_file("ipkcpc.exe", os.getcwd()), "-p", "-1234", "-h", "localhost", "-m", "tcp"],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        process = subprocess.Popen([find_file("ipkcpc", os.getcwd()), "-p", "-1234", "-h", "localhost", "-m", "tcp"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errors = process.communicate()
    return process.returncode, errors


def wrong_port_3():
    if os.name == "nt":
        process = subprocess.Popen(
            [find_file("ipkcpc.exe", os.getcwd()), "-p", "65536000000000000000", "-h", "localhost", "-m", "tcp"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        process = subprocess.Popen(
            [find_file("ipkcpc", os.getcwd()), "-p", "65536000000000000000", "-h", "localhost", "-m", "tcp"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errors = process.communicate()
    return process.returncode, errors


def missing_port():
    if os.name == "nt":
        process = subprocess.Popen([find_file("ipkcpc.exe", os.getcwd()), "-h", "localhost", "-m", "tcp"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        process = subprocess.Popen([find_file("ipkcpc", os.getcwd()), "-p", "-h", "localhost", "-m", "tcp"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errors = process.communicate()
    return process.returncode, errors


def unknown_arg():
    if os.name == "nt":
        process = subprocess.Popen([find_file("ipkcpc.exe", os.getcwd()), "-p", "2023", "-h", "localhost", "-m", "tcp", "-z"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        process = subprocess.Popen([find_file("ipkcpc", os.getcwd()), "-p", "2023", "-h", "localhost", "-m", "tcp", "-z"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errors = process.communicate()
    return process.returncode, errors


def unknown_arg_2():
    if os.name == "nt":
        process = subprocess.Popen(
            [find_file("ipkcpc.exe", os.getcwd()), "-p", "2023", "-h", "localhost", "-m", "tcp", "-z", "-y"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        process = subprocess.Popen(
            [find_file("ipkcpc", os.getcwd()), "-p", "2023", "-h", "localhost", "-m", "tcp", "-z", "-y"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errors = process.communicate()
    return process.returncode, errors


def unknown_arg_3():
    if os.name == "nt":
        process = subprocess.Popen(
            [find_file("ipkcpc.exe", os.getcwd()), "-p", "-h", "-m", "tcp", "-tcp", "-udp", "-localhost"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        process = subprocess.Popen(
            [find_file("ipkcpc", os.getcwd()), "-p", "-h", "-m", "tcp", "-tcp", "-udp", "-localhost"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errors = process.communicate()
    return process.returncode, errors


def unknown_arg_4():
    if os.name == "nt":
        process = subprocess.Popen(
            [find_file("ipkcpc.exe", os.getcwd()), "127.0.0.1", "2023", "tcp"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        process = subprocess.Popen(
            [find_file("ipkcpc", os.getcwd()), "127.0.0.1", "2023", "tcp"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errors = process.communicate()
    return process.returncode, errors


def test_wrong_protocol():
    assert wrong_protocol()[0] == 1
    if os.name == "nt":
        assert wrong_protocol()[1] == b"ERROR: invalid protocol\r\n"
    else:
        assert wrong_protocol()[1] == b"ERROR: invalid protocol\n"


def test_wrong_protocol_2():
    assert wrong_protocol_2()[0] == 1
    if os.name == "nt":
        assert wrong_protocol_2()[1] == b"ERROR: invalid protocol\r\n"
    else:
        assert wrong_protocol_2()[1] == b"ERROR: invalid protocol\n"


def test_wrong_protocol_3():
    assert wrong_protocol_3()[0] == 1
    if os.name == "nt":
        assert wrong_protocol_3()[1] == b"ERROR: invalid protocol\r\n"
    else:
        assert wrong_protocol_3()[1] == b"ERROR: invalid protocol\n"


def test_wrong_protocol_4():
    assert wrong_protocol_4()[0] == 1
    if os.name == "nt":
        assert wrong_protocol_4()[1] == b"ERROR: invalid protocol\r\n"
    else:
        assert wrong_protocol_4()[1] == b"ERROR: invalid protocol\n"


def test_missing_protocol():
    assert missing_protocol()[0] == 1
    if os.name == "nt":
        assert missing_protocol()[1] == b"ERROR: invalid number of arguments\r\n"
    else:
        assert missing_protocol()[1] == b"ERROR: invalid number of arguments\n"


def test_wrong_host():
    assert wrong_host()[0] == 1
    if os.name == "nt":
        assert wrong_host()[1] == b"ERROR: getaddrinfo failed\r\n"
    else:
        assert wrong_host()[1] == b"ERROR: getaddrinfo failed\n"


def test_wrong_host_2():
    assert wrong_host_2()[0] == 1
    if os.name == "nt":
        assert wrong_host_2()[1] == b"ERROR: getaddrinfo failed\r\n"
    else:
        assert wrong_host_2()[1] == b"ERROR: getaddrinfo failed\n"


def test_wrong_host_3():
    assert wrong_host_3()[0] == 1
    if os.name == "nt":
        assert wrong_host_3()[1] == b"ERROR: getaddrinfo failed\r\n"
    else:
        assert wrong_host_3()[1] == b"ERROR: getaddrinfo failed\n"


def test_wrong_host_4():
    assert wrong_host_4()[0] == 1
    if os.name == "nt":
        assert wrong_host_4()[1] == b"ERROR: getaddrinfo failed\r\n"
    else:
        assert wrong_host_4()[1] == b"ERROR: getaddrinfo failed\n"


def test_missing_host():
    assert missing_host()[0] == 1
    if os.name == "nt":
        assert missing_host()[1] == b"ERROR: invalid number of arguments\r\n"
    else:
        assert missing_host()[1] == b"ERROR: invalid number of arguments\n"


def test_wrong_port():
    assert wrong_port()[0] == 1
    if os.name == "nt":
        assert wrong_port()[1] == b"ERROR: invalid port\r\n"
    else:
        assert wrong_port()[1] == b"ERROR: invalid port\n"


def test_wrong_port_2():
    assert wrong_port_2()[0] == 1


def test_wrong_port_3():
    assert wrong_port_3()[0] == 1


def test_missing_port():
    assert missing_port()[0] == 1
    if os.name == "nt":
        assert missing_port()[1] == b"ERROR: invalid number of arguments\r\n"
    else:
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
