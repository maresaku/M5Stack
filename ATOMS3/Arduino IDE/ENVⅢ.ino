#include <M5Unified.h>
#include <Adafruit_SHT31.h>

Adafruit_SHT31 sht31 = Adafruit_SHT31();     // SHT3x用オブジェクト

float tmp      = 0.0;
float hum      = 0.0;

void setup() {
    auto cfg = M5.config();
    cfg.internal_imu = true;

    M5.begin(cfg);         // Init M5Atom. 
    Wire.begin(2,1);       // Initialize pin 2,1.  
    sht31.begin(0x44);     // SHT3xの初期化
    M5.Display.setTextSize(1);
    M5.Display.print(F("ENVIII Unit test"));
    Serial.println(F("ENVIII Unit test"));
}

void loop() {  
    tmp = sht31.readTemperature();   // Store the temperature obtained from shT3x.                             
    hum = sht31.readHumidity();      // Store the humidity obtained from the SHT3x.                           

    M5.Display.setCursor(0, 20);              // 文字の描画座標（カーソル位置）を設定
    M5.Display.printf(
        "Temp: %2.1f  \r\nHumi: %2.0f%%  \r\n", tmp,
        hum);
    Serial.printf(
        "Temp: %2.1f  \r\nHumi: %2.0f%%  \r\n", tmp,
        hum);
    delay(2000);
}
