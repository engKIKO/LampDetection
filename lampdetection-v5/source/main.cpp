#include <iostream>
#include "/home/thanaphat/Documents/mahidol/IoT/LampDetection/lampdetection-v5/edge-impulse-sdk/classifier/ei_run_classifier.h"

int main() {
    // Dummy input buffer (match your model’s expected input size)
    static float features[] = { /* Your data here */ };

    signal_t signal;
    int err = numpy::signal_from_buffer(features, sizeof(features) / sizeof(float), &signal);
    if (err != 0) {
        std::cerr << "Failed to create signal: " << err << std::endl;
        return 1;
    }

    ei_impulse_result_t result = { 0 };
    EI_IMPULSE_ERROR res = run_classifier(&signal, &result, false);

    if (res != EI_IMPULSE_OK) {
        std::cerr << "Failed to run classifier (" << res << ")\n";
        return 1;
    }

    std::cout << "Predictions:\n";
    for (size_t ix = 0; ix < result.classification.count; ix++) {
        std::cout << result.classification.labels[ix] << ": " << result.classification.values[ix] << "\n";
    }

    return 0;
}
