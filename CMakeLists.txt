cmake_minimum_required(VERSION 3.16)
project(test CXX)

set(CMAKE_CXX_STANDARD 20)

add_executable(ipkcpc-udp src/client.cpp)
add_executable(ipkcpc-tcp src/client.cpp)
add_executable(test src/client2.cpp)
