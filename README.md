# 🚀 Otonom Hava Savunma Sistemi (Raspberry Pi + YOLOv8)
*Mavi balon tespiti ve otomatik takip sistemi*

## 🔧 Tam Kurulum Rehberi

### 📦 Ön Gereksinimler
- **Donanım:**
  - Raspberry Pi 4 (4GB+ önerilir)
  - Pi Kamera V3
  - L298N Motor Sürücü ×2
  - SG90 Servo Motor
  - 28BYJ-48 Step Motor + ULN2003 Sürücü
  - 12V 2A harici güç kaynağı

- **Yazılım:**
  - Raspberry Pi OS (64-bit)
  - Python 3.9+

### ⚙️ 1. Donanım Bağlantıları
| Bileşen       | GPIO Pinleri           | Notlar                |
|---------------|------------------------|-----------------------|
| **Motor 1**   | ENA:22, INA:27, INB:17 | PWM kontrolü          |
| **Motor 2**   | ENB:25, INC:23, IND:24 | Ters yön aktif        |
| **Servo**     | GPIO14                 | 50Hz PWM sinyal       |
| **Step Motor**| A:17, B:27, C:22, D:18 | Half-step mod         |
| **Kamera**    | CSI port               | Picamera2 kütüphanesi |

### 💻 2. Yazılım Kurulumu
```bash
# 1. Sistemi güncelle
sudo apt update && sudo apt full-upgrade -y

# 2. Gerekli paketler
sudo apt install -y python3-picamera2 python3-opencv libopenblas-dev

# 3. Projeyi klonla
git clone https://github.com/ErguluBozkurt/AI-Air-Defence.git
cd AI-Air-Defence

# 4. Sanal ortam oluştur (Önerilir)
python3 -m venv .env
source .env/bin/activate

# 5. Bağımlılıkları yükle
pip install -r requirements.txt
