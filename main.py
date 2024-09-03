import subprocess
from azure.iot.device import IoTHubDeviceClient
import os
import json
import logging

# 디바이스 연결 문자열 가져오기
conn_str = os.getenv('DEVICE_CONNECT_STRING')
logging.info("Connection string: ", conn_str)
device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

# 디바이스 연결
device_client.connect()

def execute_command(command):
    try:
        # 명령어 실행
        logging.info(f"Executing command: {command}")
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        logging.info("Command output:", result.stdout)
        if result.stderr:
            logging.info("Command error output:", result.stderr)
    except subprocess.CalledProcessError as e:
        logging.info(f"An error occurred: {e}")

# 메시지 수신 대기
logging.info("Waiting for messages... Press Ctrl+C to exit")
while True:
    try:
        message = device_client.receive_message()
        logging.info("Message received: ", message.data)
        
        # 수신된 메시지를 명령어로 실행
        command = message.data.decode("utf-8")
        execute_command(command)
    except KeyboardInterrupt:
        # 디바이스 연결 해제
        logging.info("Disconnecting from IoT Hub")
        device_client.disconnect()
        break
    except Exception as e:
        logging.info(f"An error occurred: {e}")