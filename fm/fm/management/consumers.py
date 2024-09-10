import base64
import json
from channels.generic.websocket import AsyncWebsocketConsumer
# from django.core.files import File
# from django.core.files.storage import default_storage
# from django.conf import settings
from datetime import datetime
import os
import cv2
import numpy as np
import shutil
import subprocess


import websocket
import threading
import time

class WebSocketClient:
    def __init__(self, url):
        self.url = url
        self.ws = None
        self.flag_front = False
        self.flag_responce = None

    def on_message(self, ws, text_data):
        print("kjsdhasjkda")
        text_data_json = json.loads(text_data)
        type = text_data_json['type']
        if type == 'front_init':
            self.flag_front = True
        elif type == 'model_responce':
            print(f"CAMERA {text_data_json['camera_id']} answer is {text_data_json['answer']}")
            self.flag_responce = text_data_json['answer']


        print(f"Received message from server: {text_data}")

    def on_error(self, ws, error):
        print(f"Encountered error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        print("Connection closed")

    def on_open(self, ws):

        print("Connection established")

    def send_message_camera(self, camera_id):
        self.ws.send(data=json.dumps({
                        'type': camera_id,
                        'message': 'Take photos on camera1'
                    }))
    

    def connect(self):
        self.ws = websocket.WebSocketApp(
            self.url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        self.ws.on_open = self.on_open

        thread = threading.Thread(target=self.ws.run_forever)
        thread.start()

    def close(self):
        if self.ws:
            self.ws.close()

if __name__ == "__main__":
    # Replace with your WebSocket server URL
    websocket_url = "ws://localhost:8000/ws/control/"

    client = WebSocketClient(websocket_url)
    client.connect()
    print('FLAG: ', client.flag_front)
    # Keep the main thread alive to allow WebSocket communication
    k = 0
    try:
        while True:
            print(client.flag_front)

            if client.flag_front:
                print("ok now i am here")
                time.sleep(2) # имитация задержки перед приходом новой паллетя
                client.send_message_camera('camera1') # команда камере №1 делать фото

                while not client.flag_responce:
                    pass
                
                if client.flag_responce == 'OK':
                    client.flag_responce = None
                    # time.sleep(1)
                    client.send_message_camera('camera2')
                    print('Pallete is sended to the camera №2 zone')
                    while not client.flag_responce:
                        pass
                    if client.flag_responce == 'Defect':
                        print('Pallete is send to the replacement zone after camera2')

                elif client.flag_responce == 'Defect':
                    client.flag_responce = None
                    print('Pallete is send to the replacement zone')
                    time.sleep(3)

                # k += 1

                # if k == 3:
                    # client.close()
                    # print('here')
                    # break




                    
            # pass
            # if client.flag_front:
            #     print("ok now i am here")
            #     time.sleep(1)
            #     client.send_message_first_camera()
            #     time.sleep(1)
            #     break

    except KeyboardInterrupt:
        print("Interrupted by user, closing connection...")
        client.close()