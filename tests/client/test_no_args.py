import subprocess
import os
from tests.utility import find_file

def no_args():
    if os.name == "nt":
        process = subprocess.Popen([find_file("ipkcpc.exe", os.getcwd())], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        process = subprocess.Popen([find_file("ipkcpc", os.getcwd())], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errors = process.communicate()
    return process.returncode, errors


def test_no_args():
    assert no_args()[0] == 1
    if os.name == "nt":
        assert no_args()[1] == b"ERROR: invalid number of arguments\r\n"
    else:
        assert no_args()[1] == b"ERROR: invalid number of arguments\n"