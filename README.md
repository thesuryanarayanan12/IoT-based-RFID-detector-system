# IoT-based-RFID-detector-systemT

## System Overview

This project implements a simple and effective RFID-based access control system using the **MFRC522 RFID reader**, an **ESP8266** microcontroller, and an **MQTT messaging broker**. The system reads RFID tags and securely transmits the detected Tag IDs over a WiFi network to a backend server for authentication and logging.

---

## How It Works

1. The **MFRC522 RFID Reader**, connected to the **ESP8266**, continuously scans for nearby RFID tags.
2. When a tag is detected, the ESP8266 connects to the configured WiFi network and sends the detected **Tag ID** to an **MQTT Broker** on a designated topic.
3. A **Python backend script**, running separately, subscribes to this MQTT topic, receives the incoming Tag IDs, and checks each one against a predefined list of authorized tags.
4. The backend logs every access attempt, recording whether the tag was authorized or unauthorized, along with a timestamp for auditing purposes.

---

## Prerequisites

* **Hardware:**

  * ESP8266 microcontroller (e.g., NodeMCU or Wemos D1 Mini)
  * MFRC522 RFID Reader module
  * RFID tags/cards compatible with MFRC522

* **Software and Services:**

  * An MQTT Broker (e.g., Mosquitto) running on a local or cloud server
  * Arduino IDE or PlatformIO to program the ESP8266
  * Python 3.7+ installed on the backend machine
  * Python packages: `paho-mqtt`, `json`, `datetime` (install with `pip install paho-mqtt`)

---

## Setup Instructions

### 1. Configure the ESP8266

* Connect the MFRC522 module to the ESP8266 pins according to the wiring diagram.
* Upload the provided Arduino sketch to the ESP8266. This sketch:

  * Connects to your WiFi network (SSID and password configurable in the code)
  * Reads RFID Tag IDs
  * Publishes detected Tag IDs to the MQTT broker on a specific topic (e.g., `rfid/access`)

### 2. Set Up the MQTT Broker

* Install and run an MQTT broker like Mosquitto on your network or cloud.
* Ensure the broker is accessible by the ESP8266 and the backend Python script.

### 3. Run the Python Backend Script

* Modify the Python script to include the list of authorized Tag IDs.
* Configure the MQTT broker details and the subscribed topic.
* Run the script; it will listen for incoming Tag IDs, verify authorization, and log access attempts.

---

## Sample Output

When the Python backend receives a Tag ID, the console logs might look like this:

```
Received Tag ID: 04A3F67B8C
Access granted for Tag ID: 04A3F67B8C at 2025-06-04 14:25:10
Received Tag ID: 03B5D2187A
Access denied for Tag ID: 03B5D2187A at 2025-06-04 14:27:45
```

Logs can also be saved to a file for audit trails:

| Timestamp           | Tag ID     | Status       |
| ------------------- | ---------- | ------------ |
| 2025-06-04 14:25:10 | 04A3F67B8C | Authorized   |
| 2025-06-04 14:27:45 | 03B5D2187A | Unauthorized |

---

## Future Improvements

* Add support for dynamic tag management via a web interface or database.
* Integrate real-time notifications (e.g., email or SMS) on unauthorized access attempts.
* Enhance security with encrypted MQTT communication (TLS).
* Expand system to control physical door locks or alarms via GPIO pins on the ESP8266.

---

## References

* [MFRC522 RFID Module Documentation](https://www.nxp.com/docs/en/data-sheet/MFRC522.pdf)
* [ESP8266 Arduino Core](https://github.com/esp8266/Arduino)
* [Paho MQTT Python Client](https://pypi.org/project/paho-mqtt/)
* [Mosquitto MQTT Broker](https://mosquitto.org/)
