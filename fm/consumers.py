import json
from datetime import datetime
import os
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
        text_data_json = json.loads(text_data)
        type = text_data_json['type']
        if type == 'front_init':
            self.flag_front = True
        elif type == 'model_responce':
            print(f"CAMERA {text_data_json['camera_id']} answer on picture {text_data_json['photo_id']} is {text_data_json['answer']}")
            self.flag_responce = text_data_json['answer']


        print(f"Received message from server: {text_data}")

    def on_error(self, ws, error):
        print(f"Encountered error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        print("Connection closed")

    def on_open(self, ws):

        print("Connection established")

    def send_message_camera(self, camera_id, timestamp):
        self.ws.send(data=json.dumps({
                        'type': 'camera',
                        'camera_id': camera_id,
                        'pallete_id': timestamp, 
                        'message': 'Take photos on camera1'
                    }))
        
    def new_pallete_came(self):
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

        self.ws.send(data=json.dumps({
                        'type': 'get_new_pallete',
                        'message': 'New pallete has arrived!',
                        'pallete_id': timestamp
                    }))
        return timestamp

    

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
    websocket_url = os.environ.get("WS_CONTROL_URL")

    client = WebSocketClient(websocket_url)
    client.connect()
    k = 0
    try:
        while True:
            time.sleep(0.05)
            if client.flag_front:
                time.sleep(2) # имитация задержки перед приходом новой паллета
                pallete_id = client.new_pallete_came() # сигнал, что пришел новый паллет
                client.send_message_camera(1, pallete_id)  # команда камере №1 делать фото

                while not client.flag_responce: # ожидаем ответа пайплайна
                    time.sleep(0.05)
                    pass
                
                if client.flag_responce == 'OK':
                    client.flag_responce = None
                    # time.sleep(1)
                    client.send_message_camera(2, pallete_id)
                    print('Pallete is sended to the camera №2 zone')
                    while not client.flag_responce:
                        time.sleep(0.05)
                        pass
                    if client.flag_responce == 'Defect':
                        client.flag_responce = None
                        print('Pallete is send to the replacement zone after camera2')
                    # time.sleep(3)

                elif client.flag_responce == 'Defect':
                    client.flag_responce = None
                    print('Pallete is send to the replacement zone')
                    time.sleep(3)

    except KeyboardInterrupt:
        print("Interrupted by user, closing connection...")
        client.close()