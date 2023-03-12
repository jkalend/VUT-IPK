import pytest
import subprocess


def no_args():
    process = subprocess.Popen(["cmake-build-debug/ipkcpc"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errors = process.communicate()
    return process.returncode, errors


def test_no_args():
    assert no_args()[0] == 1
    assert no_args()[1] == b"ERROR: invalid number of arguments\n"