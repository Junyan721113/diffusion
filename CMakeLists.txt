cmake_minimum_required (VERSION 3.8)

project ("sas-vision-2023")

find_package(OpenCV REQUIRED)
# opencv include path: /usr/local/include/opencv4

include_directories(${OpenCV_INCLUDE_DIRS})
link_libraries(${OpenCV_LIBS})

add_executable (test "test.cpp")
