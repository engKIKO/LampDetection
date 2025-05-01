from datetime import datetime
import time
import cv2
import edge_impulse_linux
import mqttHandel
from edge_impulse_linux.image import ImageImpulseRunner
from lampLogger import time_is_night, log_broken_lamp
from LampDetectionBuffer import LampDetectionBuffer
import lampLogger
# from mqttHandel import LDR_is_night


MODEL_PATH = '/home/thanaphat/Documents/mahidol/IoT/LampDetection/modelfile.eim'

# Define camera zones for each lamp (update these based on your camera layout)
lamp_zones = {
    # 'Lamp1': (0, 0, 160, 120),      # x1, y1, x2, y2
    # 'Lamp2': (160, 0, 320, 120),
    # 'Lamp3': (0, 120, 160, 240),
    'Lamp4': (160, 120, 250, 180)
}

# Log buffer init
detection_buffer = LampDetectionBuffer(interval_seconds=60)

def main():
    mqttHandel.start()
    with ImageImpulseRunner(MODEL_PATH) as runner:
        model_info = runner.init()
        labels = model_info['model_parameters']['labels']
        model_type = model_info['model_parameters']['model_type']
        print(f"Model type: {model_type}")
        
        cap = cv2.VideoCapture('/dev/video2')  # Change 

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


                # Inside your loop after getting results
                if 'bounding_boxes' in results['result']:
                    for box in results['result']['bounding_boxes']:
                        label = box['label']
                        confidence = box['value']
                        ldrValues = mqttHandel.get_ldr_value()
                        tempTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        print(f"[{lamp_name}] → Detected: {label} (confidence: {confidence:.2f})")
                        detection_buffer.add_detection(label)

                        # Check for "off" label during night
                        # if is_night(current_hour=20) and label.lower() == "off":
                        #     log_broken_lamp(lamp_id=1, label=label)
                        if datetime.now().second % 30 == 0:
                            # if detection_buffer.should_log_broken_lamp(is_night_time=True):  # or determine time by your logic
                            #     log_broken_lamp(lamp_id="Lamp1",label=label, status="broken", reason="majority 'off' detections during night")
                            # detection_buffer.clear()
                            
                            if label.lower() == "on":
                                if time_is_night(): # if time is night
                                    if mqttHandel.LDR_is_night() == True:
                                        # mqttHandel.publish_log(log_broken_lamp(lamp_id=lamp_name, label=label , status="normally runnig",reason=f"majority 'on' detections during night from Time and LDR values is {ldrValues}"))
                                        lampLogger.log_lamp_status(lamp_id=lamp_name,status="runnig",confidence=confidence,reason="Normally lamp running",ldr_value=ldrValues)
                                        detection_buffer.clear()
                                    else:
                                        # mqttHandel.publish_log(log_broken_lamp(lamp_id=lamp_name, label=label ,status="abnormally",reason=f"majority 'off' detections during night from Time only LDR values  is {ldrValues}"))
                                        lampLogger.log_lamp_status(lamp_id=lamp_name,status="runnig",confidence=confidence,reason=f"A Time is night {tempTime} not releate with  LDR is Days {ldrValues} Lamp is running",ldr_value=ldrValues,level="Err")
                                        detection_buffer.clear()

                                else : # time is  days

                                    if mqttHandel.LDR_is_night() == True:
                                        # mqttHandel.publish_log(log_broken_lamp(lamp_id=lamp_name, label=label ,status="abnormally",reason="majority 'off' detections during night from LDR only"))
                                        lampLogger.log_lamp_status(lamp_id=lamp_name,status="runnig",confidence=confidence,reason=f"B Time is days {tempTime} not releate with LDR is Night {ldrValues} Lamp is running",ldr_value=ldrValues,level="Err")
                                        detection_buffer.clear()
                                    else:
                                        # mqttHandel.publish_log(log_broken_lamp(lamp_id=lamp_name, label=label ,status="abnormally",reason="majority 'off' detections but not to know reason "))
                                        lampLogger.log_lamp_status(lamp_id=lamp_name,status="runnig",confidence=confidence,reason=f"C Time is days {tempTime}  releate with LDR is Days {ldrValues} but Lamp shuould not running",ldr_value=ldrValues,level="Warn")
                                        detection_buffer.clear()


                            elif label.lower() == "off":
                                if time_is_night():
                                    if mqttHandel.LDR_is_night() == True:
                                        # mqttHandel.publish_log(log_broken_lamp(lamp_id=lamp_name, label=label , status="broken",reason=f"majority 'off' detections during night from Time and LDR values is {ldrValues}"))
                                        lampLogger.log_lamp_status(lamp_id=lamp_name,status="broken",confidence=confidence,reason=f"D Time is Night {tempTime}  releate with LDR is Night{ldrValues} but Lamp si not running",ldr_value=ldrValues,level="Warn")
                                        detection_buffer.clear()
                                    else:
                                        # mqttHandel.publish_log(log_broken_lamp(lamp_id=lamp_name, label=label ,status="broken",reason=f"majority 'off' detections during night from Time only LDR values  is {ldrValues}"))
                                        lampLogger.log_lamp_status(lamp_id=lamp_name,status="broken",confidence=confidence,reason=f"E Time is Night {tempTime} not releate with LDR is Days{ldrValues} but Lamp is should running",ldr_value=ldrValues,level="Err")
                                        detection_buffer.clear()
                                else :
                                    if mqttHandel.LDR_is_night() == True:
                                        # mqttHandel.publish_log(log_broken_lamp(lamp_id=lamp_name, label=label ,status="broken",reason="majority 'off' detections during night from LDR only"))
                                        lampLogger.log_lamp_status(lamp_id=lamp_name,status="broken",confidence=confidence,reason=f"F Time is Days {tempTime} not releate with LDR is Night{ldrValues} but Lamp is should running",ldr_value=ldrValues,level="Err")
                                        detection_buffer.clear()
                                    else : 
                                        # mqttHandel.publish_log(log_broken_lamp(lamp_id=lamp_name, label=label ,status="broken",reason="majority 'off' detections during night from LDR only"))
                                        lampLogger.log_lamp_status(lamp_id=lamp_name,status="broken",confidence=confidence,reason=f"G Time is Days {tempTime}  releate with LDR is Days {ldrValues} Lamp is not running",ldr_value=ldrValues,level="Info")
                                        detection_buffer.clear()

                            else:
                                # mqttHandel.publish_log(log_broken_lamp(lamp_id=lamp_name, label=label ,status="broken",reason="majority 'off' detections but not to know reason "))
                                lampLogger.log_lamp_status(lamp_id=lamp_name,status="unknow",confidence=confidence,reason=f"H Not detection Time is Days {tempTime}  releate with LDR is Days {ldrValues}",ldr_value=ldrValues,level="Err")
                                detection_buffer.clear()

                elif 'classification' in results['result']:
                    # In case you also support classification models
                    label = max(results['result']['classification'], key=results['result']['classification'].get)
                    print(f"[Lamp1] → Classification Label: {label}")
                    if label.lower() == "off":
                        if time_is_night(current_hour=20):
                            if mqttHandel.LDR_is_night() == True:
                                mqttHandel.publish_log(log_broken_lamp(lamp_id=1, label=label , status="broken",reason="majority 'off' detections during night from Time and LDR"))
                                print("hand1")
                            else:
                                mqttHandel.publish_log(log_broken_lamp(lamp_id=1, label=label ,status="broken",reason="majority 'off' detections during night from Time only"))
                                print("hand2")
                        elif mqttHandel.LDR_is_night() == True:
                            mqttHandel.publish_log(log_broken_lamp(lamp_id=1, label=label ,status="broken",reason="majority 'off' detections during night from LDR only"))
                            print("hand3")
                        else:
                            mqttHandel.publish_log(log_broken_lamp(lamp_id=1, label=label ,status="broken",reason="majority 'off' detections but not to know reason "))
                            print("hand4")
                    # Check every N seconds if we should log
                    # if datetime.now().second % 60 == 0:
                    #     if detection_buffer.should_log_broken_lamp(is_night_time=True):  # or determine time by your logic
                    #         log_lamp_status(lamp_id="Lamp1", status="broken", reason="majority 'off' detections during night")
                    #     detection_buffer.clear()

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
        mqttHandel.stop()
        


if __name__ == '__main__':
    main()
