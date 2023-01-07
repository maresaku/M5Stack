#include <M5Unified.h>
#include "Adafruit_SGP30.h"

Adafruit_SGP30 sgp;
long last_millis = 0;

void setup() {
    auto cfg = M5.config();
    cfg.internal_imu = true;
  
    M5.begin(cfg);
    
    M5.Display.setTextSize(1);               // テキストサイズを変更
    M5.Display.setCursor(20, 0);
    M5.Display.print("TVOC TEST");       // 画面
    if (!sgp.begin()) {  // Init the sensor. 初始化传感器
        M5.Display.print("Sensor not found");
        while (1)
            ;
    }
    M5.Display.setCursor(0, 20);
    M5.Display.print("\nInitialization...");
}

void loop() {
    if (!sgp.IAQmeasure()) {  // Commands the sensor to take a single eCO2/VOC
                              // measurement.  命令传感器进行一次eCO2/VOC测量
        Serial.println("Measurement failed");
        return;
    }
    M5.Display.setCursor(0, 10);
    M5.Display.printf("TVOC:%d ppb\n", sgp.TVOC);
    M5.Display.printf("eCO2:%d ppm\n", sgp.eCO2);
    delay(500);
}
