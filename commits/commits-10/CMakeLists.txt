cmake_minimum_required(VERSION 3.16)
project(IPK CXX C)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_C_STANDARD 11)

if (WIN32)
add_executable(ipkcpc src/client.cpp src/utils.cpp src/utils.h src/getopt/getopt.cpp src/getopt/getopt.h)
add_executable(ipkcpd src/server.cpp src/utils.cpp src/utils.h src/getopt/getopt.cpp src/getopt/getopt.h)
else()
add_executable(ipkcpc src/client.cpp src/utils.cpp src/utils.h)
add_executable(ipkcpd src/server.cpp src/utils.cpp src/utils.h)
endif ()
