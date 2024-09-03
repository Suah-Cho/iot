import signal
import subprocess
from azure.iot.device import IoTHubDeviceClient
import os
import logging

# 디바이스 연결 문자열 가져오기
conn_str = os.getenv('DEVICE_CONNECT_STRING')
logging.info(f"Device connection string: {conn_str}")
device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

# 디바이스 연결
device_client.connect()

def command(command):
    try:
        logging.info(f"Excuting command: {command}")
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logging.info(f"Command executed successfully", result.stdout)
        if result.stderr:
            logging.error(f"Command Error output: {result.stderr}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error: {e}")

# 메시지 수신 대기
logging.info("Waiting for messages... Press Ctrl+C to exit")
while True:
    try:
        message = device_client.receive_message()
        logging.info("Message received: ", message.data)

        # 수신된 메세지를 기반으로 업데이트 작업 실행
        com = message.data['command']
        command(command=com)
    except KeyboardInterrupt:
        # 디바이스 연결 해제
        logging.info("Disconnecting from IoT Hub")
        device_client.disconnect()
        break
    except Exception as e:
        logging.error(f"An error occurred: {e}")

