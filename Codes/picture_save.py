from picamera2 import Picamera2
import cv2
import time

# Kamera başlatma
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (720, 480), "format": "RGB888"})
picam2.configure(config)
picam2.start()

counter = 1  # Resim numaralandırma için sayaç
last_capture_time = time.time()  # Son çekim zamanı

cv2.namedWindow("Canlı Görüntü", cv2.WINDOW_NORMAL)  # Tek pencere oluştur

while True:
    frame = picam2.capture_array()  # Kameradan görüntü al

    # Canlı video akışı penceresi (Tekrar tekrar açılmaz, sürekli güncellenir)
    cv2.imshow("Canlı Görüntü", frame)

    # 5 saniyede bir resim kaydetme
    if time.time() - last_capture_time >= 5:
        filename = f"image_{counter}.jpg"
        cv2.imwrite(filename, frame)
        print(f"{filename} kaydedildi.")
        counter += 1
        last_capture_time = time.time()  # Zamanı sıfırla

    # Çıkış için 'q' tuşuna basılırsa programı kapat
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
