import paho.mqtt.client as mqtt
import time

# --- CONFIGURATION ---
MQTT_BROKER = "localhost"  # Change to your broker's IP address
MQTT_PORT = 1883
MQTT_TOPIC = "rfid/access"

# A simple in-memory "database" of authorized RFID tags
AUTHORIZED_TAGS = {
    "0A 7B 1C 9D": "Alice",
    "5E 3F 8A 2B": "Bob",
    "DE C0 AD 1F": "Charlie"
}

# --- MQTT CALLBACKS ---
def on_connect(client, userdata, flags, rc):
    """Callback function for when the client connects to the broker."""
    if rc == 0:
        print(f"Successfully connected to MQTT Broker and subscribed to topic '{MQTT_TOPIC}'")
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"Failed to connect, return code {rc}\n")

def on_message(client, userdata, msg):
    """Callback function for when a message is received from the broker."""
    tag_id = msg.payload.decode("utf-8")
    print(f"\n[LOG] RFID Tag Detected: {tag_id}")

    # Check if the received tag is in our list of authorized tags
    if tag_id in AUTHORIZED_TAGS:
        user = AUTHORIZED_TAGS[tag_id]
        print(f"[INFO] Access GRANTED for {user} (Tag ID: {tag_id})")
    else:
        print(f"[WARNING] Access DENIED for unknown Tag ID: {tag_id}")

# --- MAIN SCRIPT ---
if __name__ == "__main__":
    # Create an MQTT client instance
    client = mqtt.Client()

    # Assign the callback functions
    client.on_connect = on_connect
    client.on_message = on_message

    print("Connecting to MQTT Broker...")
    try:
        # Connect to the broker
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        # Start the network loop to process callbacks. This is a blocking call.
        client.loop_forever()
    except ConnectionRefusedError:
        print("[ERROR] Connection to MQTT broker was refused. Is the broker running?")
    except KeyboardInterrupt:
        print("\n[INFO] Disconnecting from MQTT Broker.")
        client.disconnect()
