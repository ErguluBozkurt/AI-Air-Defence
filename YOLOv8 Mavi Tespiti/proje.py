import cv2
from ultralytics import YOLO


model_path = "19. YOLOv8 Mavi Tespiti/best.pt" # best yolu

model = YOLO(model_path)

cap = cv2.VideoCapture(0)
while True:
  success, frame = cap.read()
  if(success):
    frame = cv2.resize(frame, (720,480)) # width değerine göre height değerini otomatik seçiyor
    results = model(frame)[0]
    
    for result in results.boxes.data.tolist():

      x1,y1,x2,y2,score,class_id = result
      x1,y1,x2,y2,class_id = int(x1), int(y1), int(x2), int(y2), int(class_id)
      if(score>0.5):
        cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
        class_name = results.names[class_id]
        score = score * 100
        text = class_name + ":" + str(round(score,2)) + "%"
        cv2.putText(frame, text, (x1,y1-10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0), 1)
       
        # Get object's center coordinates
        obj_center_x = (x1 + x2) // 2
        obj_center_y = (y1 + y2) // 2
        
        diff_x = 360 - obj_center_x # ekranın ortası - tespit edilen nesnenin orta noktası -300 ile +300
        diff_y = 240 - obj_center_y # -180 ile +180

        print("X-axis stepper motor : ", diff_x)
        print("Y-axis stepper motor : ", diff_y)
        
      else:
        cv2.putText(frame, "Object Not Detected", (10, 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.75, (0, 255, 255), 1)
    cv2.imshow("Kamera", frame)

    if(cv2.waitKey(1) & 0xFF == ord("q")):
     break

cap.release()
cv2.destroyAllWindows()




