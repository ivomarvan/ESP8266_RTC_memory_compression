cmake_minimum_required(VERSION 3.6)
project(compressedMemory)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
set(SOURCE_FILES
       main.cpp )
include_directories(cpp)

add_executable(compressedMemory ${SOURCE_FILES})

project(compressedMemoryTest)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
set(SOURCE_FILES
        cpp/unit-tests/tests-main.cpp cpp/unit-tests/test-BitsStack.cpp)
include_directories(cpp cpp/libs/Catch/single_include)

add_executable(compressedMemoryTest ${SOURCE_FILES})
