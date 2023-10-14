cmake_minimum_required(VERSION 3.16)
project(IPK CXX C)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_C_STANDARD 11)

if (WIN32)
add_executable(ipkcpc Project-1/ipkcpc.cpp Project-1/utils.cpp Project-1/utils.h
        Project-1/getopt/getopt.cpp Project-1/getopt/getopt.h)
add_executable(ipkcpd Project-2/IOTA.cpp Project-2/IOTA.h Project-1/utils.cpp Project-1/utils.h
        Project-2/server.cpp Project-2/server.h Project-2/TCPServer.cpp Project-2/TCPServer.h Project-2/UDPServer.cpp
        Project-2/UDPServer.h Project-2/UDPServer.cpp Project-1/getopt/getopt.cpp Project-1/getopt/getopt.h)
else()
add_executable(ipkcpc Project-1/ipkcpc.cpp Project-1/utils.cpp Project-1/utils.h)
add_executable(ipkcpd Project-2/IOTA.cpp Project-2/IOTA.h Project-1/utils.cpp Project-1/utils.h
        Project-2/server.cpp Project-2/server.h Project-2/TCPServer.cpp Project-2/TCPServer.h Project-2/UDPServer.cpp
        Project-2/UDPServer.h Project-2/UDPServer.cpp)
endif ()
