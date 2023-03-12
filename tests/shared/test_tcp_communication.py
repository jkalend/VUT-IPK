import pytest
import subprocess

def correct_handshake_and_leave(server_tcp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "tcp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"HELLO\nBYE\n", timeout=3)
    return process.returncode, outs, errors


def simple_solve_plus(server_tcp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "tcp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"HELLO\nSOLVE (+ 1 2)\nBYE\n", timeout=3)
    return process.returncode, outs, errors


def simple_solve_minus(server_tcp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "tcp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"HELLO\nSOLVE (- 1 2)\nBYE\n", timeout=3)
    return process.returncode, outs, errors


def simple_solve_multiply(server_tcp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "tcp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"HELLO\nSOLVE (* 1 2)\nBYE\n", timeout=3)
    return process.returncode, outs, errors


def simple_solve_divide(server_tcp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "tcp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"HELLO\nSOLVE (/ 1 2)\nBYE\n", timeout=3)
    return process.returncode, outs, errors


def inner_expression(server_tcp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "tcp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"HELLO\nSOLVE (+ 1 (* 2 3))\nBYE\n", timeout=3)
    return process.returncode, outs, errors


def double_inner_expression(server_tcp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "tcp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"HELLO\nSOLVE (+ 1 (* 2 (+ 3 4)))\nBYE\n", timeout=3)
    return process.returncode, outs, errors


def two_inner_expression(server_tcp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "tcp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"HELLO\nSOLVE (+ 1 (* 2 (+ 3 4)) (* 5 6))\nBYE\n", timeout=3)
    return process.returncode, outs, errors


def complex_expression(server_tcp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "tcp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"HELLO\nSOLVE (+ 1 (* 2 (+ 3 4)) (* 5 6) (/ 7 8) (/ 1 1))\nBYE\n", timeout=3)
    return process.returncode, outs, errors


def complex_expression2(server_tcp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "tcp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"HELLO\nSOLVE (+ 1 (* 45 (+ 3 4)) (* 3 6) (/ 7 8) (/ 0 1) (/ 9 100))\nBYE\n", timeout=3)
    return process.returncode, outs, errors


def long_expression(server_tcp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "tcp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"HELLO\nSOLVE (+ 100 (+ 1 1) (+ 1 1) (+ 1 1) (+ 1 1) (+ 1 1) (+ 1 1) (+ 1 1) (+ 1 1) (+ 1 1) (+ 1 1) (+ 1 1))\nBYE\n", timeout=3)
    return process.returncode, outs, errors


def long_expression2(server_tcp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "tcp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"HELLO\nSOLVE (* 1 1 1 1 1 1 1 1 1 1 1 0)\nBYE\n", timeout=3)
    return process.returncode, outs, errors


def missing_expression(server_tcp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "tcp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"HELLO\nSOLVE\nBYE\n", timeout=3)
    return process.returncode, outs, errors


def missing_solve(server_tcp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "tcp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"HELLO\n(+ 1 2)\nBYE\n", timeout=3)
    return process.returncode, outs, errors


def too_short_expression(server_tcp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "tcp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"HELLO\nSOLVE (+ 1)\n", timeout=3)
    return process.returncode, outs, errors


def too_short_expression2(server_tcp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "tcp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"HELLO\nSOLVE (+)\n", timeout=3)
    return process.returncode, outs, errors


def empty_expression(server_tcp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "tcp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"HELLO\nSOLVE ()\n", timeout=3)
    return process.returncode, outs, errors


def empty_expression2(server_tcp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "tcp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"HELLO\nSOLVE (  )\n", timeout=3)
    return process.returncode, outs, errors


def too_many_spaces(server_tcp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "tcp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"HELLO\nSOLVE (+ 1 2  )\n", timeout=3)
    return process.returncode, outs, errors


def too_many_spaces2(server_tcp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "tcp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"HELLO\nSOLVE ( + 1 2 )\n", timeout=3)
    return process.returncode, outs, errors


def too_many_spaces3(server_tcp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "tcp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"HELLO\nSOLVE  (+ 1 2 )\n", timeout=3)
    return process.returncode, outs, errors


def too_many_spaces4(server_tcp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "tcp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"HELLO\nSOLVE ( + 1 2)\n", timeout=3)
    return process.returncode, outs, errors


def complex_expression_with_divide_by_zero(server_tcp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "tcp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"HELLO\nSOLVE (+ 1 (* 2 (+ 3 4)) (* 5 6) (/ 7 0))\nBYE\n", timeout=3)
    return process.returncode, outs, errors


def missing_left_bracket(server_tcp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "tcp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"HELLO\nSOLVE + 1 2)\n", timeout=3)
    return process.returncode, outs, errors


def missing_right_bracket(server_tcp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "tcp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"HELLO\nSOLVE (+ 1 2\n", timeout=3)
    return process.returncode, outs, errors


def too_long_message(server_tcp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "tcp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"HELLO\nSOLVE (+ 1 2)\n" * 100000, timeout=3)
    process.communicate(input=b"BYE\n", timeout=3)
    return process.returncode, outs, errors


def test_correct_handshake_and_leave(server_tcp):
    ret, outs, errors = correct_handshake_and_leave(server_tcp)
    assert ret == 0
    assert outs == b"HELLO\nBYE\n"
    assert errors == b""


def test_simple_solve(server_tcp):
    ret, outs, errors = simple_solve_plus(server_tcp)
    assert ret == 0
    assert outs == b"HELLO\nRESULT 3.000000\nBYE\n"
    assert errors == b""


def test_simple_solve_minus(server_tcp):
    ret, outs, errors = simple_solve_minus(server_tcp)
    assert ret == 0
    assert outs == b"HELLO\nRESULT -1.000000\nBYE\n"
    assert errors == b""


def test_simple_solve_multiply(server_tcp):
    ret, outs, errors = simple_solve_multiply(server_tcp)
    assert ret == 0
    assert outs == b"HELLO\nRESULT 2.000000\nBYE\n"
    assert errors == b""


def test_simple_solve_divide(server_tcp):
    ret, outs, errors = simple_solve_divide(server_tcp)
    assert ret == 0
    assert outs == b"HELLO\nRESULT 0.500000\nBYE\n"
    assert errors == b""


def test_inner_expression(server_tcp):
    ret, outs, errors = inner_expression(server_tcp)
    assert ret == 0
    assert outs == b"HELLO\nRESULT 7.000000\nBYE\n"
    assert errors == b""


def test_double_inner_expression(server_tcp):
    ret, outs, errors = double_inner_expression(server_tcp)
    assert ret == 0
    assert outs == b"HELLO\nRESULT 15.000000\nBYE\n"
    assert errors == b""


def test_two_inner_expression(server_tcp):
    ret, outs, errors = two_inner_expression(server_tcp)
    assert ret == 0
    assert outs == b"HELLO\nRESULT 45.000000\nBYE\n"
    assert errors == b""


def test_complex_expression(server_tcp):
    ret, outs, errors = complex_expression(server_tcp)
    assert ret == 0
    assert outs == b"HELLO\nRESULT 46.875000\nBYE\n"
    assert errors == b""


def test_complex_expression2(server_tcp):
    ret, outs, errors = complex_expression2(server_tcp)
    assert ret == 0
    assert outs == b"HELLO\nRESULT 334.965000\nBYE\n"
    assert errors == b""


def test_long_expression(server_tcp):
    ret, outs, errors = long_expression(server_tcp)
    assert ret == 0
    assert outs == b"HELLO\nRESULT 122.000000\nBYE\n"
    assert errors == b""


def test_long_expression2(server_tcp):
    ret, outs, errors = long_expression2(server_tcp)
    assert ret == 0
    assert outs == b"HELLO\nRESULT 0.000000\nBYE\n"
    assert errors == b""


def test_missing_expression(server_tcp):
    ret, outs, errors = missing_expression(server_tcp)
    assert ret == 1
    assert outs == b"HELLO\nBYE\n"
    assert errors != b""


def test_missing_solve(server_tcp):
    ret, outs, errors = missing_solve(server_tcp)
    assert ret == 1
    assert outs == b"HELLO\nBYE\n"
    assert errors != b""


def test_too_short_expression(server_tcp):
    ret, outs, errors = too_short_expression(server_tcp)
    assert ret == 1
    assert outs == b"HELLO\nBYE\n"
    assert errors != b""


def test_too_short_expression2(server_tcp):
    ret, outs, errors = too_short_expression2(server_tcp)
    assert ret == 1
    assert outs == b"HELLO\nBYE\n"
    assert errors != b""


def test_too_many_spaces(server_tcp):
    ret, outs, errors = too_many_spaces(server_tcp)
    assert ret == 1
    assert outs == b"HELLO\nBYE\n"
    assert errors != b""


def test_too_many_spaces2(server_tcp):
    ret, outs, errors = too_many_spaces2(server_tcp)
    assert ret == 1
    assert outs == b"HELLO\nBYE\n"
    assert errors != b""


def test_too_many_spaces3(server_tcp):
    ret, outs, errors = too_many_spaces3(server_tcp)
    assert ret == 1
    assert outs == b"HELLO\nBYE\n"
    assert errors != b""


def test_too_many_spaces4(server_tcp):
    ret, outs, errors = too_many_spaces4(server_tcp)
    assert ret == 1
    assert outs == b"HELLO\nBYE\n"
    assert errors != b""


def test_complex_expression_with_divide_by_zero(server_tcp):
    ret, outs, errors = complex_expression_with_divide_by_zero(server_tcp)
    assert ret == 1
    assert outs == b"HELLO\nBYE\n"
    assert errors != b""


def test_missing_left_bracket(server_tcp):
    ret, outs, errors = missing_left_bracket(server_tcp)
    assert ret == 1
    assert outs == b"HELLO\nBYE\n"
    assert errors != b""


def test_missing_right_bracket(server_tcp):
    ret, outs, errors = missing_right_bracket(server_tcp)
    assert ret == 1
    assert outs == b"HELLO\nBYE\n"
    assert errors != b""


def too_long_message(server_tcp):
    ret, outs, errors = too_long_message(server_tcp)
    assert ret == 0
    assert outs == b"HELLO\nBYE\n"
    assert errors != b""
