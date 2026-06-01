
#include <WiFi.h>
#include <HTTPClient.h>
#include <BLEDevice.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>

const char* ssid = "";
const char* password = "";
const char* serverName = "http://192.168.x.x/rssi"; // IP DHCP do servidor

String scanner_id = "AP_01"; // AP_02, AP_03, etc.
String target_name = "BLE_BEACON";
int scanTime = 5;
float A = -62.0

class MyAdvertisedDeviceCallbacks: public BLEAdvertisedDeviceCallbacks {
    void onResult(BLEAdvertisedDevice advertisedDevice) {
      if (advertisedDevice.getName() == target_name) {
        int rssi = advertisedDevice.getRSSI();
        float distance = pow(10.0, ((A - rssi) / (10 * 2)));

        Serial.print("Encontrado: ");
        Serial.print(target_name);
        Serial.print(" | RSSI: ");
        Serial.print(rssi);
        Serial.print(" dBm | Est. Distância: ");
        Serial.print(distance, 2);
        Serial.println(" m");

        if(WiFi.status() == WL_CONNECTED) {
          HTTPClient http;
          http.begin(serverName);
          http.addHeader("Content-Type", "application/json");

          String json = "{\"scanner_id\":\"" + scanner_id + "\",\"beacon_id\":\"" + target_name + "\",\"rssi\":" + String(rssi) + ",\"distance\":" + String(distance) + "}";

          int httpResponseCode = http.POST(json);
          http.end();
        }
      }
    }
};

void setup() {
  Serial.begin(115200);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("conectado ao wifi");

  BLEDevice::init("");
  BLEScan* pBLEScan = BLEDevice::getScan();
  pBLEScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks());
  pBLEScan->setActiveScan(true);
  pBLEScan->setInterval(100);
  pBLEScan->setWindow(99);
}

void loop() {
  BLEScan* pBLEScan = BLEDevice::getScan();
  pBLEScan->start(scanTime, false);
  delay((scanTime + 1) * 1000);
}
