cmake_minimum_required(VERSION 3.10)
project(LampDetection)

set(CMAKE_CXX_STANDARD 11)

# Base path to your project
set(BASE_DIR /home/thanaphat/Documents/mahidol/IoT/LampDetection/lampdetection-v5)

# Add include directories
include_directories(
    ${BASE_DIR}/edge-impulse-sdk
    ${BASE_DIR}/model-parameters
    ${BASE_DIR}/tflite-model
    ${BASE_DIR}/source
)

# Add executable with correct source files
add_executable(app
    ${BASE_DIR}/source/main.cpp
    ${BASE_DIR}/tflite-model/tflite_learn_3_compiled.cpp
)

