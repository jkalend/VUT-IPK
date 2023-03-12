import pytest
import subprocess
from time import sleep
import asyncio
import os
from contextlib import closing
import sys
import os
import select


def simple_solve_plus(server_udp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "udp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"(+ 1 2)\n", timeout=3)
    process.send_signal(subprocess.signal.SIGINT)
    process.wait(5)
    return process.returncode, outs, errors


def simple_solve_minus(server_udp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "udp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"(- 1 2)\n", timeout=3)
    process.send_signal(subprocess.signal.SIGINT)
    process.wait(5)
    return process.returncode, outs, errors


def simple_solve_multiply(server_udp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "udp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"(* 1 2)\n", timeout=3)
    process.send_signal(subprocess.signal.SIGINT)
    process.wait(5)
    return process.returncode, outs, errors


def simple_solve_divide(server_udp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "udp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"(/ 1 2)\n", timeout=3)
    return process.returncode, outs, errors


def inner_expression(server_udp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "udp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"(+ 1 (* 2 3))\n", timeout=3)
    process.send_signal(subprocess.signal.SIGINT)
    process.wait(5)
    return process.returncode, outs, errors


def double_inner_expression(server_udp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "udp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"(+ 1 (* 2 (+ 3 4)))\n", timeout=3)
    process.send_signal(subprocess.signal.SIGINT)
    process.wait(5)
    return process.returncode, outs, errors


def two_inner_expression(server_udp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "udp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"(+ 1 (* 2 (+ 3 4)) (* 5 6))\n", timeout=3)
    process.send_signal(subprocess.signal.SIGINT)
    process.wait(5)
    return process.returncode, outs, errors


def complex_expression(server_udp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "udp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"(+ 1 (* 2 (+ 3 4)) (* 5 6) (/ 7 8) (/ 1 1))\n", timeout=3)
    process.send_signal(subprocess.signal.SIGINT)
    process.wait(5)
    return process.returncode, outs, errors


def complex_expression2(server_udp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "udp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"(+ 1 (* 45 (+ 3 4)) (* 3 6) (/ 7 8) (/ 0 1) (/ 9 100))\n", timeout=3)
    process.send_signal(subprocess.signal.SIGINT)
    process.wait(5)
    return process.returncode, outs, errors


def long_expression(server_udp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "udp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"(+ 100 (+ 1 1) (+ 1 1) (+ 1 1) (+ 1 1) (+ 1 1) (+ 1 1) (+ 1 1) (+ 1 1) (+ 1 1) (+ 1 1) (+ 1 1))\n", timeout=3)
    process.send_signal(subprocess.signal.SIGINT)
    process.wait(5)
    return process.returncode, outs, errors


def long_expression2(server_udp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "udp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"(* 1 1 1 1 1 1 1 1 1 1 1 0)\n", timeout=3)
    process.send_signal(subprocess.signal.SIGINT)
    process.wait(5)
    return process.returncode, outs, errors


def missing_expression(server_udp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "udp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"SOLVE\n", timeout=3)
    process.send_signal(subprocess.signal.SIGINT)
    process.wait(5)
    return process.returncode, outs, errors


def redundant_solve(server_udp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "udp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"SOLVE (+ 1 2)\n", timeout=3)
    process.send_signal(subprocess.signal.SIGINT)
    process.wait(5)
    return process.returncode, outs, errors


def too_short_expression(server_udp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "udp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"(+ 1)\n", timeout=3)
    process.send_signal(subprocess.signal.SIGINT)
    process.wait(5)
    return process.returncode, outs, errors


def too_short_expression2(server_udp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "udp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"(+)\n", timeout=3)
    process.send_signal(subprocess.signal.SIGINT)
    process.wait(5)
    return process.returncode, outs, errors


def empty_expression(server_udp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "udp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"()\n", timeout=3)
    process.send_signal(subprocess.signal.SIGINT)
    process.wait(5)
    return process.returncode, outs, errors


def empty_expression2(server_udp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "udp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"(  )\n", timeout=3)
    process.send_signal(subprocess.signal.SIGINT)
    process.wait(5)
    return process.returncode, outs, errors


def too_many_spaces(server_udp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "udp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"(+ 1 2  )\n", timeout=3)
    process.send_signal(subprocess.signal.SIGINT)
    process.wait(5)
    return process.returncode, outs, errors


def too_many_spaces2(server_udp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "udp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"( + 1 2 )\n", timeout=3)
    process.send_signal(subprocess.signal.SIGINT)
    process.wait(5)
    return process.returncode, outs, errors


def too_many_spaces3(server_udp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "udp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b" (+ 1 2 )\n", timeout=3)
    process.send_signal(subprocess.signal.SIGINT)
    process.wait(5)
    return process.returncode, outs, errors


def too_many_spaces4(server_udp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "udp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"( + 1 2)\n", timeout=3)
    process.send_signal(subprocess.signal.SIGINT)
    process.wait(5)
    return process.returncode, outs, errors


def complex_expression_with_divide_by_zero(server_udp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "udp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"(+ 1 (* 2 (+ 3 4)) (* 5 6) (/ 7 0))\n", timeout=3)
    process.send_signal(subprocess.signal.SIGINT)
    process.wait(5)
    return process.returncode, outs, errors


def missing_left_bracket(server_udp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "udp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"+ 1 2)\n", timeout=3)
    process.send_signal(subprocess.signal.SIGINT)
    process.wait(5)
    return process.returncode, outs, errors


def missing_right_bracket(server_udp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "udp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"(+ 1 2\n", timeout=3)
    process.send_signal(subprocess.signal.SIGINT)
    process.wait(5)
    return process.returncode, outs, errors


def too_long_message(server_udp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "udp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"a" * 10000 + b"\n", timeout=3)
    process.send_signal(subprocess.signal.SIGINT)
    process.wait(5)
    return process.returncode, outs, errors


def continue_after_error(server_udp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "udp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    outs, errors = process.communicate(input=b"(+ 1 2\n(+ 1 2)\n", timeout=3)
    process.send_signal(subprocess.signal.SIGINT)
    process.wait(5)
    return process.returncode, outs, errors


def no_disconnect(server_udp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "udp"],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, bufsize=0)

    sent = 0
    outs, errors = "", ""
    while sent != 3:
        for index, io in enumerate(select.select([process.stdout.fileno(), process.stderr.fileno()], [process.stdin.fileno()], [])):
            if index == 0 and io and io[0] == process.stdout.fileno():
                outs += process.stdout.readline().decode("utf-8")
                sent += 1
                sleep(1)
            if index == 1 and io and io[0] == process.stdin.fileno():
                process.stdin.write(b"(+ 1 2)\n")
            if index == 2 and io and io[0] == process.stderr.fileno():
                errors += process.stderr.readline().decode("utf-8")

    process.send_signal(subprocess.signal.SIGINT)
    process.wait()
    return process.returncode, outs, errors


def many_requests(server_udp):
    process = subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "udp"],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, bufsize=0)

    sent = 0
    outs, errors = "", ""
    while sent != 10000:
        for index, io in enumerate(
                select.select([process.stdout.fileno(), process.stderr.fileno()], [process.stdin.fileno()], [])):
            if index == 0 and io and io[0] == process.stdout.fileno():
                outs += process.stdout.readline().decode("utf-8")
                sent += 1
            if index == 1 and io and io[0] == process.stdin.fileno():
                process.stdin.write(b"(+ 1 2)\n")
            if index == 2 and io and io[0] == process.stderr.fileno():
                errors += process.stderr.readline().decode("utf-8")

    process.send_signal(subprocess.signal.SIGINT)
    process.wait()
    return process.returncode, outs, errors


def many_clients(server_udp):
    processes = []
    for i in range(30):
        processes.append(subprocess.Popen(["cmake-build-debug/ipkcpc", "-p", "2023", "-h", "localhost", "-m", "udp"],
                                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, bufsize=0))

    for process in processes:
        process.stdin.write(b"(+ 1 2)\n")

    outs, errors = "", ""
    res = 0
    for process in processes:
        outs += process.stdout.readline().decode("utf-8")
        process.send_signal(subprocess.signal.SIGINT)
        process.wait()
        res += process.returncode

    return res, outs, errors


def many_clients_many_requests(server_udp):
    def find_file(filename, search_path):
        for root, dir, files in os.walk(search_path):
            if filename in files:
                return os.path.join(root, filename)

    processes = []
    for i in range(30):
        processes.append(subprocess.Popen(["python3", find_file("udp_spammer.py", os.getcwd())], stdout=subprocess.PIPE))

    outs = ""
    sleep(2)
    for process in processes:
        process.wait(60)
        outs += process.stdout.read().decode("utf-8")

    return outs


def test_simple_solve(server_udp):
    ret, outs, errors = simple_solve_plus(server_udp)
    assert ret == 0
    assert outs == b"OK:3.000000\n"
    assert errors == b""


def test_simple_solve_minus(server_udp):
    ret, outs, errors = simple_solve_minus(server_udp)
    assert ret == 0
    assert outs == b"OK:-1.000000\n"
    assert errors == b""


def test_simple_solve_multiply(server_udp):
    ret, outs, errors = simple_solve_multiply(server_udp)
    assert ret == 0
    assert outs == b"OK:2.000000\n"
    assert errors == b""


def test_simple_solve_divide(server_udp):
    ret, outs, errors = simple_solve_divide(server_udp)
    assert ret == 0
    assert outs == b"OK:0.500000\n"
    assert errors == b""


def test_inner_expression(server_udp):
    ret, outs, errors = inner_expression(server_udp)
    assert ret == 0
    assert outs == b"OK:7.000000\n"
    assert errors == b""


def test_double_inner_expression(server_udp):
    ret, outs, errors = double_inner_expression(server_udp)
    assert ret == 0
    assert outs == b"OK:15.000000\n"
    assert errors == b""


def test_two_inner_expression(server_udp):
    ret, outs, errors = two_inner_expression(server_udp)
    assert ret == 0
    assert outs == b"OK:45.000000\n"
    assert errors == b""


def test_complex_expression(server_udp):
    ret, outs, errors = complex_expression(server_udp)
    assert ret == 0
    assert outs == b"OK:46.875000\n"
    assert errors == b""


def test_complex_expression2(server_udp):
    ret, outs, errors = complex_expression2(server_udp)
    assert ret == 0
    assert outs == b"OK:334.965000\n"
    assert errors == b""


def test_long_expression(server_udp):
    ret, outs, errors = long_expression(server_udp)
    assert ret == 0
    assert outs == b"OK:122.000000\n"
    assert errors == b""


def test_long_expression2(server_udp):
    ret, outs, errors = long_expression2(server_udp)
    assert ret == 0
    assert outs == b"OK:0.000000\n"
    assert errors == b""


def test_missing_expression(server_udp):
    ret, outs, errors = missing_expression(server_udp)
    assert ret == 0
    assert outs == b""
    assert errors != b""


def test_redundant_solve(server_udp):
    ret, outs, errors = redundant_solve(server_udp)
    assert ret == 0
    assert outs == b""
    assert errors != b""


def test_too_short_expression(server_udp):
    ret, outs, errors = too_short_expression(server_udp)
    assert ret == 0
    assert outs == b""
    assert errors != b""


def test_too_short_expression2(server_udp):
    ret, outs, errors = too_short_expression2(server_udp)
    assert ret == 0
    assert outs == b""
    assert errors != b""


def test_too_many_spaces(server_udp):
    ret, outs, errors = too_many_spaces(server_udp)
    assert ret == 0
    assert outs == b""
    assert errors != b""


def test_too_many_spaces2(server_udp):
    ret, outs, errors = too_many_spaces2(server_udp)
    assert ret == 0
    assert outs == b""
    assert errors != b""


def test_too_many_spaces3(server_udp):
    ret, outs, errors = too_many_spaces3(server_udp)
    assert ret == 0
    assert outs == b""
    assert errors != b""


def test_too_many_spaces4(server_udp):
    ret, outs, errors = too_many_spaces4(server_udp)
    assert ret == 0
    assert outs == b""
    assert errors != b""


def test_complex_expression_with_divide_by_zero(server_udp):
    ret, outs, errors = complex_expression_with_divide_by_zero(server_udp)
    assert ret == 0
    assert outs == b""
    assert errors != b""


def test_missing_left_bracket(server_udp):
    ret, outs, errors = missing_left_bracket(server_udp)
    assert ret == 0
    assert outs == b""
    assert errors != b""


def test_missing_right_bracket(server_udp):
    ret, outs, errors = missing_right_bracket(server_udp)
    assert ret == 0
    assert outs == b""
    assert errors != b""


def test_too_long_message(server_udp):
    ret, outs, errors = too_long_message(server_udp)
    assert ret == 0
    assert outs == b""
    assert errors != b""


def test_continue_after_error(server_udp):
    ret, outs, errors = continue_after_error(server_udp)
    assert ret == 0
    assert outs == b"OK:3.000000\n"
    assert errors != b""


def test_no_disconnect(server_udp):
    res, outs, errors = no_disconnect(server_udp)
    assert res == 0
    assert outs == "OK:3.000000\n" * 3
    assert errors == ""


def test_many_requests(server_udp):
    res, outs, errors = many_requests(server_udp)
    assert res == 0
    assert outs == "OK:3.000000\n" * 10000
    assert errors == ""


def test_many_clients(server_udp):
    res, outs, errors = many_clients(server_udp)
    assert res == 0
    assert outs == "OK:3.000000\n" * 100
    assert errors == ""


def test_many_clients_many_requests(server_udp):
    outs = many_clients_many_requests(server_udp)
    assert outs == "OK:3.000000\n" * 50 * 30

