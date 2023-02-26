cmake_minimum_required(VERSION 3.16)
project(template CXX)

set(CMAKE_CXX_STANDARD 20)

add_executable(template src/client.cpp)
add_executable(test src/client2.cpp)
