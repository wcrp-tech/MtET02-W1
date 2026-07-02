#include <WiFi.h>

// WiFi Config
char ssid[] = "wcrpw";      // ใส่ชื่อ WiFi
char pass[] = "wcrpwarn";      // ใส่รหัสผ่าน WiFi

const char* host = "192.168.1.10";  // IP Server
const uint16_t port = 2000;         // Port Server

WiFiClient client;

unsigned long previousMillis = 0;
const long SendTime = 2000; // 2 วินาที

void setup()
{
  Serial.begin(115200);

  // กำหนด seed สำหรับเลขสุ่ม
  randomSeed(micros());

  WiFi.mode(WIFI_STA);

  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, pass);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi Connected!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  Serial.print("Connecting to Server... ");

  if (client.connect(host, port))
  {
    Serial.println("Connected");
  }
  else
  {
    Serial.println("Failed");
  }
}

void loop()
{
  // ถ้าหลุดการเชื่อมต่อ ให้เชื่อมใหม่
  if (!client.connected())
  {
    Serial.println("Reconnecting...");

    if (client.connect(host, port))
    {
      Serial.println("Connected to Server");
    }

    delay(1000);
    return;
  }

  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= SendTime)
  {
    previousMillis = currentMillis;

    int randomNumber = random(0, 11); // สุ่ม 0-10

    client.println(randomNumber);

    Serial.print("Sent: ");
    Serial.println(randomNumber);
  }

  // รับข้อมูลจาก Server (ถ้ามี)
  if (client.available())
  {
    String response = client.readStringUntil('\n');

    Serial.print("Received: ");
    Serial.println(response);
  }
}