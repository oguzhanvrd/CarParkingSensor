from machine import Pin
import utime

# LED pinleri için liste oluşturuluyor
led_pins = [Pin(pin, Pin.OUT) for pin in range(10, 13)]  # GPIO pinleri 10-12 arasında olan LED'ler kullanılacak

trigger = Pin(3, Pin.OUT)
echo = Pin(4, Pin.IN)
# Buzzer'ın bağlandığı GPIO pin numarası (Örneğin: GP28 pinine bağlandıysa)
BUZZER_PIN = 28

# Buzzer'ı kontrol etmek için pin oluştur
buzzer = Pin(BUZZER_PIN, Pin.OUT)

def mesafe_olc():
    trigger.low()
    utime.sleep_us(2)
    trigger.high()
    utime.sleep_us(10)
    trigger.low()
    while echo.value() == 0:
        signaloff = utime.ticks_us()
    while echo.value() == 1:
        signalon = utime.ticks_us()
    sure = signalon - signaloff
    distance = (sure * 0.0343) / 2
    return distance

def buzzer_control(distance):
    # Mesafe azaldıkça buzzer hızı artır
    if distance < 25:
        # Buzzer hızını mesafe değerine göre ayarla
        buzzer.on()
        buzzer_time = max(0, 0.1 - (distance * 0.01))  # Mesafe azaldıkça süreyi kısalt
        utime.sleep(buzzer_time)  # Buzzer süresi
        buzzer.off()
    elif distance < 5:
        buzzer.on()
    else:
        buzzer.off()

def led_control(distance):
    # Eğer mesafe 25cm'den küçükse LED'leri kontrol et
    if distance < 25:
        # Mesafe 0-25cm arasında olduğunda LED'lerin yanma durumunu belirle
        for i, led in enumerate(led_pins):
            if distance >= (i + 1) * 5:  # Her LED için sınır değeri kontrolü
                led.off()  # LED'i yak
            else:
                led.on()  # LED'i söndür
    else:
        # 25cm'den uzaksa tüm LED'leri kapat
        for led in led_pins:
            led.off()  # Tüm LED'leri söndür

while True:
    mesafe = mesafe_olc()
    print("Nesneye olan uzaklık ", mesafe, "cm")
    led_control(mesafe)
    buzzer_control(mesafe)
    utime.sleep(0.5)
