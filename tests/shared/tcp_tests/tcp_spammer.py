#!/usr/bin/env python3
import subprocess
import select
import sys
import os


def find_file(filename, search_path):
    for root, dir, files in os.walk(search_path):
        if filename in files:
            return os.path.join(root, filename)


process = subprocess.Popen([find_file("ipkcpc", os.getcwd()), "-p", "2023", "-h", "localhost", "-m", "tcp"],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, bufsize=0)

sent = 0
outs, errors = "", ""
process.stdin.write(b"HELLO\n")
while sent != 21:
    for index, io in enumerate(
            select.select([process.stdout.fileno(), process.stderr.fileno()], [process.stdin.fileno()], [])):
        if index == 0 and io and io[0] == process.stdout.fileno():
            outs += process.stdout.readline().decode("utf-8")
            sent += 1
        if index == 1 and io and io[0] == process.stdin.fileno():
            if sent == 20:
                process.stdin.write(b"BYE\n")
            else:
                process.stdin.write(b"SOLVE (+ 1 2)\n")
        if index == 2 and io and io[0] == process.stderr.fileno():
            errors += process.stderr.readline().decode("utf-8")

process.send_signal(subprocess.signal.SIGINT)
process.wait(5)
if errors:
    sys.exit(1)
print(outs, end="")
