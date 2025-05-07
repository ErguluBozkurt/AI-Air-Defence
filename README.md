# 🚀 Otonom Hava Savunma Sistemi (Raspberry Pi 4B + YOLOv8)
*Mavi balon tespiti ve otomatik takip sistemi*

Bu proje, Raspberry Pi kullanılarak mavi renkli nesnelerin gerçek zamanlı olarak tespit edilmesi, step motor ile nesneye yönelme, nesneye ulaşıldığında servo motor ve DC motorlarla silah sisteminin devreye girmesi ile atış gerçekleştirilmesini sağlayan **görsel tabanlı bir otomasyon sistemidir**. YOLOv8 modeli ile görüntü üzerinde nesne tespiti yapılmakta ve buna göre donanım bileşenleri eş zamanlı olarak kontrol edilmektedir.

---

## 📌 Proje Amacı

- **Görüntü İşleme**: Raspberry Pi üzerinde çalışan kamera ile gerçek zamanlı görüntü yakalanması.
- **Yapay Zeka**: YOLOv8 nesne tespiti algoritmasıyla mavi renkteki nesnelerin algılanması.
- **Hareket Mekaniği**: Step motorlarla kameranın nesneye yönelmesi.
- **Tepki Mekanizması**: Servo motorun nesne merkezdeyken çalışması.
- **Hareket Komutu**: Nesne algılandıktan sonra atış için DC motorların belirli süre çalıştırılması.

---

## 🧠 Algoritma Akışı

1. PiCamera2 aracılığıyla görüntü alınır.
2. YOLOv8 modeli ile her kare üzerinde nesne tespiti yapılır.
3. Eğer "mavi nesne" tespit edilirse:
   - Nesnenin konumu çerçeve ortasına göre analiz edilir.
   - Gerekirse step motorlar ile yön düzeltmesi yapılır.
4. Nesne merkezdeyse:
   - DC motorlar çalıştırılır.
   - Servo motor çalıştırılır.
6. Eğer nesne tespit edilmezse, sistem bekleme moduna geçer.

---

## 🧰 Donanım Gereksinimleri

| Bileşen              | Açıklama                                               |
|----------------------|--------------------------------------------------------|
| Raspberry Pi 4       | Ana kontrol birimi                                     |
| Raspberrypi Kamera   | Görüntü alma işlemini gerçekleştirir                   |
| 2 Adet Step Motor    | Kamera sisteminin X-Y düzleminde yönelmesini sağlar    |
| 1 Adet Servo Motor   | Hedef merkezdeyken tetiklenir                          |
| 2 Adet DC Motor      | Tespit sonrası belirli süre hareket eder               |
| L298N Motor Sürücü   | DC motorları kontrol etmek için kullanılır             |
| Jumper Kabloları     | Bağlantılar için                                       |
| Harici Güç Kaynağı   | DC motorlar için önerilir                              |

---

## 🔌 GPIO Pin Bağlantı Şeması

| Bileşen         | GPIO Pinleri         | Açıklama                         |
|------------------|-----------------------|----------------------------------|
| Step Motor X     | GPIO 5, 6, 13, 26     | X ekseninde yönelme              |
| Step Motor Y     | GPIO 1, 7, 8, 12      | Y ekseninde yönelme              |
| Servo Motor      | GPIO 16               | Hedef merkezdeyse çalışır        |
| DC Motor 1/2     | GPIO 17, 22, 23, 24, 25, 27 | L298N sürücü ile yön kontrolü |

---

## 🖥️ Yazılım Gereksinimleri

- Python 3.x (>=3.7)
- `OpenCV` — Görüntü işleme
- `ultralytics` — YOLOv8 modeli için
- `picamera2` — Raspberry Pi kamerası desteği
- `RPi.GPIO` — GPIO pin kontrolü
- `numpy` — Görüntü matris işlemleri

---

## ⚙️ Kurulum Adımları

1. Raspberry Pi işletim sisteminizi güncelleyin:
   ```bash
   sudo apt update && sudo apt upgrade
   sudo apt install python3-pip
   pip install -r requirements.txt
