#include <SPI.h>
#include <MFRC522.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// -- PIN DEFINITIONS --
#define RST_PIN D3 // Configurable, set to your RST pin
#define SS_PIN  D4 // Configurable, set to your SS/SDA pin

// -- WIFI CREDENTIALS --
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// -- MQTT BROKER CONFIG --
const char* mqtt_server = "your_mqtt_broker_ip"; // IP address of your MQTT broker
const char* mqtt_topic = "rfid/access";

// -- GLOBAL OBJECTS --
MFRC522 mfrc522(SS_PIN, RST_PIN);
WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;

// Function to connect to MQTT
void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP8266_RFID_Client")) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000); // Wait 5 seconds before retrying
    }
  }
}

void setup() {
  Serial.begin(115200); // Initialize serial comms
  SPI.begin();          // Init SPI bus
  mfrc522.PCD_Init();   // Init MFRC522 card

  // Connect to Wi-Fi
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected.");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  // Connect to MQTT
  client.setServer(mqtt_server, 1883);
}

void loop() {
  // Ensure client is connected to MQTT broker
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // Look for new cards
  if (!mfrc522.PICC_IsNewCardPresent() || !mfrc522.PICC_ReadCardSerial()) {
    delay(50);
    return;
  }

  // A card has been detected, read its UID
  String tag_id = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    tag_id.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
    tag_id.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  tag_id.trim();
  tag_id.toUpperCase();

  Serial.print("Tag detected! UID: ");
  Serial.println(tag_id);

  // Publish the tag ID to the MQTT topic
  client.publish(mqtt_topic, tag_id.c_str());

  // Halt PICC and delay to prevent spamming
  mfrc522.PICC_HaltA();
  delay(2000); // Wait 2 seconds before next read
}
