import pytest
import subprocess


def only_one_arg():
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errors = process.communicate()
    if errors == b'ERROR: invalid number of arguments\n' and process.returncode == 1:
        raise ConnectionError


def only_two_args():
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errors = process.communicate()
    if errors == b'ERROR: invalid number of arguments\n' and process.returncode == 1:
        raise ConnectionError


def no_args():
    process = subprocess.Popen(["cmake-build-debug/ipkcpc"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errors = process.communicate()
    if errors == b'ERROR: invalid number of arguments\n' and process.returncode == 1:
        raise ConnectionError


def test_no_args():
    with pytest.raises(ConnectionError):
        no_args()


def test_only_two_args():
    with pytest.raises(ConnectionError):
        only_two_args()


def test_only_one_arg():
    with pytest.raises(ConnectionError):
        only_one_arg()
