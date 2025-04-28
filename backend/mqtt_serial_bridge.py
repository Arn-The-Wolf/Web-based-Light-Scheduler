import paho.mqtt.client as mqtt
import serial
import json
import time
from datetime import datetime

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "light/schedule"
SERIAL_PORT = "COM3"  # Change to your Arduino port
SERIAL_BAUDRATE = 9600

current_schedule = None

# Connect to Arduino
ser = serial.Serial(SERIAL_PORT, SERIAL_BAUDRATE, timeout=1)
time.sleep(2)  # Wait for Arduino to reset

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with code {rc}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    global current_schedule
    try:
        payload = json.loads(msg.payload.decode())
        print(f"Received schedule: {payload}")
        current_schedule = payload
    except Exception as e:
        print(f"Error parsing MQTT message: {e}")

def check_and_send():
    global current_schedule
    if not current_schedule:
        return
    now = datetime.now().strftime('%H:%M')
    on_time = current_schedule.get('on')
    off_time = current_schedule.get('off')
    if now == on_time:
        print("Sending ON command to Arduino")
        ser.write(b'1')
        time.sleep(1)
    elif now == off_time:
        print("Sending OFF command to Arduino")
        ser.write(b'0')
        time.sleep(1)

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()
    try:
        while True:
            check_and_send()
            time.sleep(30)  # Check every 30 seconds
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        client.loop_stop()
        ser.close()

if __name__ == "__main__":
    main()
