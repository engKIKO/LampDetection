import time
import cv2
import edge_impulse_linux
from edge_impulse_linux.image import ImageImpulseRunner
from lampLogger import is_night, log_broken_lamp


MODEL_PATH = '/home/thanaphat/Documents/mahidol/IoT/LampDetection/modelfile.eim'

# Define camera zones for each lamp (update these based on your camera layout)
lamp_zones = {
    'Lamp1': (0, 0, 160, 120),      # x1, y1, x2, y2
    # 'Lamp2': (160, 0, 320, 120),
    # 'Lamp3': (0, 120, 160, 240),
    # 'Lamp4': (160, 120, 320, 240)
}

def main():
    with ImageImpulseRunner(MODEL_PATH) as runner:
        model_info = runner.init()
        labels = model_info['model_parameters']['labels']
        model_type = model_info['model_parameters']['model_type']
        print(f"Model type: {model_type}")
        
        cap = cv2.VideoCapture('/dev/video2')  # Change as needed

        if not cap.isOpened():
            print("Failed to open camera.")
            return

        print("Starting lamp detection...")

        while True:
            time.sleep(0.2)
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame.")
                break

            # Loop through each defined lamp zone
            for lamp_name, (x1, y1, x2, y2) in lamp_zones.items():
                zone_frame = frame[y1:y2, x1:x2]

                try:
                    features, _ = runner.get_features_from_image(zone_frame)
                    results = runner.classify(features)
                except Exception as e:
                    print(f"Error processing {lamp_name}: {e}")
                    continue

                # Display results based on model type
                # if model_type == 'classification' and 'classification' in results['result']:
                #     label = max(results['result']['classification'],
                #                 key=results['result']['classification'].get)
                #     if is_night(current_hour=20) and label.lower() == "off":
                #         print("Logging lamp as broken...")
                #         log_broken_lamp(lamp_id=1, label=label)
                #     confidence = results['result']['classification'][label]
                #     print(f"[{lamp_name}] → {label} ({confidence:.2f})")
                # elif model_type == 'object_detection' and 'bounding_boxes' in results['result']:
                #     print(f"[{lamp_name}] → Detections:", results['result']['bounding_boxes'])
                #     if is_night(current_hour=20) and label.lower() == "off":
                #         log_broken_lamp(lamp_id=1, label=label)
                # elif 'anomaly' in results['result']:
                #     print(f"[{lamp_name}] → Anomaly score:", results['result']['anomaly']['score'])
                # else:
                #     print(f"[{lamp_name}] → Unexpected result format:", results)

                # Inside your loop after getting results
                if 'bounding_boxes' in results['result']:
                    for box in results['result']['bounding_boxes']:
                        label = box['label']
                        confidence = box['value']
                        
                        print(f"[Lamp1] → Detected: {label} (confidence: {confidence:.2f})")

                        # Check for "off" label during night
                        if is_night(current_hour=20) and label.lower() == "off":
                            log_broken_lamp(lamp_id=1, label=label)

                elif 'classification' in results['result']:
                    # In case you also support classification models
                    label = max(results['result']['classification'], key=results['result']['classification'].get)
                    print(f"[Lamp1] → Classification Label: {label}")

                    if is_night(current_hour=20) and label.lower() == "off":
                        log_broken_lamp(lamp_id=1, label=label)

                else:
                    print(f"[Lamp1] → Unexpected result format: {results}")


                # Draw rectangle for the zone on the main frame
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, lamp_name, (x1 + 5, y1 + 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

            # Display the full frame with overlays
            cv2.imshow('Lamp Detection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
        


if __name__ == '__main__':
    main()
