import cv2
import edge_impulse_linux
from edge_impulse_linux.image import ImageImpulseRunner

MODEL_PATH = '/home/thanaphat/Documents/mahidol/IoT/LampDetection/modelfile.eim'

def main():
    with ImageImpulseRunner(MODEL_PATH) as runner:
        model_info = runner.init()
        labels = model_info['model_parameters']['labels']

        cap = cv2.VideoCapture('/dev/video2')   # USB camera (use 1 or IP URL for other sources)

        if not cap.isOpened():
            print("Failed to open camera.")
            return

        print("Starting lamp detection...")

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame.")
                break

            features, cropped = runner.get_features_from_image(frame)
            results = runner.classify(features)
           

            if 'classification' in results['result']:
                print("Prediction:", results['result']['classification'])
            elif 'bounding_boxes' in results['result']:
                print("Detections:", results['result']['bounding_boxes'])
            elif 'anomaly' in results['result']:
                print("Anomaly score:", results['result']['anomaly']['score'])
            else:
                print("Unexpected result format:", results)
                # Add logic here: threshold, lamp mapping, etc.

            # Optional: show frame
            cv2.imshow('Lamp Detection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
