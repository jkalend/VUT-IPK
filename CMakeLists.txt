cmake_minimum_required(VERSION 3.16)
project(test CXX C)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_C_STANDARD 11)

add_executable(ipkcpc-udp src/client.cpp src/utils.cpp src/utils.h)
add_executable(ipkcpc-tcp src/client.cpp src/utils.cpp src/utils.h)
add_executable(server-tcp src/server.cpp src/utils.cpp src/utils.h)
add_executable(server-udp src/server.cpp src/utils.cpp src/utils.h)
add_executable(test3 ipkpd/Stubs/cpp/DemoTcp/client.c)