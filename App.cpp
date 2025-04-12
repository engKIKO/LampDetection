#include <iostream>
#include <fstream>
#include "tensorflow/lite/interpreter.h"
#include "tensorflow/lite/kernels/register.h"
#include "tensorflow/lite/model.h"

int main() {
    // Load the model (make sure your model.tflite is in the same directory)
    const char* modelFilename = "model.tflite";
    auto model = tflite::FlatBufferModel::BuildFromFile(modelFilename);
    if (!model) {
        std::cerr << "Failed to load model " << modelFilename << std::endl;
        return -1;
    }
    std::cout << "Model loaded successfully." << std::endl;
    
    // Build the interpreter
    tflite::ops::builtin::BuiltinOpResolver resolver;
    std::unique_ptr<tflite::Interpreter> interpreter;
    tflite::InterpreterBuilder(*model, resolver)(&interpreter);
    if (!interpreter) {
        std::cerr << "Failed to construct interpreter" << std::endl;
        return -1;
    }
    
    // Allocate tensor buffers.
    if (interpreter->AllocateTensors() != kTfLiteOk) {
        std::cerr << "Failed to allocate tensors!" << std::endl;
        return -1;
    }
    
    // For example, set input data (modify as needed)
    float* input = interpreter->typed_input_tensor<float>(0);
    // Fill in your input values; here we simply set them to zero
    for (int i = 0; i < interpreter->input_tensor(0)->bytes / sizeof(float); i++) {
        input[i] = 0.0f;
    }
    
    // Run inference
    if (interpreter->Invoke() != kTfLiteOk) {
        std::cerr << "Error during inference" << std::endl;
        return -1;
    }
    
    // Process the output
    float* output = interpreter->typed_output_tensor<float>(0);
    std::cout << "Inference output: " << output[0] << std::endl;
    
    return 0;
}
