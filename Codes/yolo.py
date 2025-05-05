import cv2
from ultralytics import YOLO
from picamera2 import Picamera2
import time


# Set up the camera with Picam
picam2 = Picamera2()
picam2.preview_configuration.main.size = (720, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

# Load YOLOv8
model = YOLO("best.pt")

while True:
    # Capture a frame from the camera
    frame = picam2.capture_array()
    
    # Run YOLO model on the captured frame and store the results
    # results = model(frame)

    results = model(frame)[0]

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result
        x1, y1, x2, y2, class_id = int(x1), int(y1), int(x2), int(y2), int(class_id)

        if score > 0.2:
            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            class_name = results.names[class_id]
            score = score * 100
            text = class_name + ":" + str(round(score, 2)) + "%"
            cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.75, (0, 255, 255), 1)

            # Get object's center coordinates
            obj_center_x = (x1 + x2) // 2
            obj_center_y = (y1 + y2) // 2
            
            diff_x = 360 - obj_center_x # ekranın ortası - tespit edilen nesnenin orta noktası
            diff_y = 240 - obj_center_y

            print("X-axis stepper motor : ", diff_x)
            print("Y-axis stepper motor : ", diff_y)
            
        else:
            cv2.putText(frame, "Object Not Detected", (10, 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.75, (0, 255, 255), 1)

    cv2.imshow("Image", frame)

    # Check if "x" key is pressed to trigger servo movement
    key = cv2.waitKey(1) & 0xFF
    # Exit the loop when "q" is pressed
    if key == ord("q"):
        break


cv2.destroyAllWindows()
