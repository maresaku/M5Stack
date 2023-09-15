from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

import network
import time
import ujson
import urequests

#OLED
WIDTH  = 128
HEIGHT = 64
i2c = I2C(0, scl=Pin(26), sda=Pin(32), freq=200000) 
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

#misaki
fcolor = 1
#フォントサイズの倍数
fsize = 1
#フォントのビットマップ表示
def show_bitmap(oled, fd, x, y, color, size):
    for row in range(0, 7):
        for col in range(0, 7):
            if (0x80 >> col) & fd[row]:
                oled.fill_rect(int(x + col * size), int(y + row * size), size, size, color)
    oled.show()

#wifi接続
ssid = 'WifiのID'
Password = 'password'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid,Password)
wlan.isconnected()
while not wlan.isconnected():
    pass
#print('listening on', wlan.ifconfig()[0])

weathercode = {
00 : "Clear sky",
01 : "Mainly clear",
02 : "Mainly clear",
03 : "Mainly clear",
45 : "Fog",
48 : "Fog",
51 : "Drizzle",
53 : "Drizzle",
55 : "Drizzle",
56 : "Freezing Drizzle",
57 : "Freezing Drizzle",
61 : "Rain",
63 : "Rain",
65 : "Rain",
66 : "Freezing Rain",
67 : "Freezing Rain",
71 : "Snow fall",
73 : "Snow fall",
75 : "Snow fall",
77 : "Snow grains",
80 : "Rain showers",
81 : "Rain showers",
82 : "Rain showers",
85 : "Snow showers",
86 : "Snow showers",
95 : "Thunderstorm",
96 : "Thunderstorm",
99 : "Thunderstorm",
}

#緯度と経度(東京)
lat = '35.69'
lon = '139.47'

while True:
    #url
    url = "https://api.open-meteo.com/v1/forecast?latitude=" + lat + "&longitude=" + lon + "&daily=weathercode,temperature_2m_max,temperature_2m_min&forecast_days=3&timezone=Asia%2FTokyo"
    json_data = urequests.get(url)
    #print(json_data.json())

    i = 0
    Date = []
    Weather = []
    Temp_max = []
    Temp_min = []
    Pops_max = []
    for i in range(3):
        #日付    
        date = [str(json_data.json().get('daily').get('time')[i])]
        Date = Date + date
        #天気    
        weather = [weathercode[int(json_data.json().get('daily').get('weathercode')[i])]]
        Weather = Weather + weather
        #最高気温   
        temp_max = [str(json_data.json().get('daily').get('temperature_2m_max')[i])]
        Temp_max = Temp_max + temp_max
        #最低気温   
        temp_min = [str(json_data.json().get('daily').get('temperature_2m_min')[i])]
        Temp_min = Temp_min + temp_min

    #今日
    #日付
    str_1 = "[" + Date[0] + "]"     
    #天気
    str_2 = " " + Weather[0]
    #気温
    str_3 = " " + Temp_max[0] + "[C]" + "/" + Temp_min[0] + "[C]"
    
    #明日
    #日付
    str_4 = "[" + Date[1] + "]"
    #天気
    str_5 = " " + Weather[1]
    #気温
    str_6 = " "  +  Temp_max[1] + "[C]" + "/" + Temp_min[1] + "[C]"
    oled.fill(0)
    oled.text(str_1, 0, 0)
    oled.text(str_2, 0, 10)
    oled.text(str_3, 0, 20)
    oled.text(str_4, 0, 30)
    oled.text(str_5, 0, 40)
    oled.text(str_6, 0, 50)
    oled.show()
    time.sleep(3600)
