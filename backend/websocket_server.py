import asyncio
import websockets
import json
import subprocess

MQTT_TOPIC = "light/schedule"
MQTT_BROKER = "localhost"
MQTT_PORT = 1883

async def handler(websocket, path):
    async for message in websocket:
        try:
            data = json.loads(message)
            on_time = data.get("on")
            off_time = data.get("off")
            if not on_time or not off_time:
                await websocket.send("Invalid schedule data.")
                continue
            # Publish to MQTT using mosquitto_pub
            payload = json.dumps({"on": on_time, "off": off_time})
            result = subprocess.run([
                "mosquitto_pub",
                "-h", MQTT_BROKER,
                "-p", str(MQTT_PORT),
                "-t", MQTT_TOPIC,
                "-m", payload
            ], capture_output=True, text=True)
            if result.returncode == 0:
                await websocket.send("Schedule forwarded to MQTT.")
            else:
                await websocket.send(f"Failed to publish to MQTT: {result.stderr}")
        except Exception as e:
            await websocket.send(f"Error: {str(e)}")

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("WebSocket server running on ws://0.0.0.0:8765")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
