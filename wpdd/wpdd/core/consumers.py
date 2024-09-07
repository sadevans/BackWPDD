import base64
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.files import File
from django.core.files.storage import default_storage
from django.conf import settings
from datetime import datetime
import os
import cv2
import numpy as np
import shutil
import subprocess
# from pipelines.pipelines import DetectDefectsPipeline


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            'file_watch_group',
            self.channel_name
        )
        await self.accept()


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'file_watch_group',
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.send(text_data=json.dumps({
                    'message': 'Success'
                }))


    async def send_file_change_notification(self, event):
        # Send message to WebSocket
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        await get_photos(timestamp)
        all_photos = os.listdir(f"{settings.MEDIA_ROOT}/{timestamp}")
        all_photos_abs = []
        encoded_photos_list = []

        for file in all_photos:
            print(file)
            try:
                photo_path = os.path.join(f"{settings.MEDIA_ROOT}/{timestamp}", file)
                all_photos_abs.append(photo_path)
                print(photo_path)
                in_data_bytes = open(photo_path, "rb").read()

                if in_data_bytes:
                    encoded_photo_in = base64.b64encode(in_data_bytes).decode('ascii')
                    encoded_photos_list.append(encoded_photo_in)
                #     await self.send(text_data=json.dumps({
                #         'type': 'image',
                #         'message': 'Success',
                #         'in_image_url': encoded_photo_in
                #     }))

                # else:
                #     await self.send(text_data=json.dumps({
                #         'error': 'Unable to read image'
                #     }))

                # if len(encoded_photos_list) > 0 :
                #     await self.send(text_data=json.dumps({
                #             'type': 'image_batch',
                #             'message': 'Success',
                #             'images': encoded_photos_list
                #         }))
                # else:
                #     await self.send(text_data=json.dumps({
                #         'error': 'Unable to read images'
                #     }))
                    # await self.send(text_data=json.dumps({
                    # 'error': str(e)
                    # }))


            except Exception as e:
                await self.send(text_data=json.dumps({
                    'error': str(e)
                }))

        if len(encoded_photos_list) > 0 :
                await self.send(text_data=json.dumps({
                        'type': 'image_batch',
                        'message': 'Success',
                        'images': encoded_photos_list
                    }))
        else:
            await self.send(text_data=json.dumps({
                'error': 'Unable to read images'
            }))

        # if not pipeline:
        #     pipeline = DetectDefectsPipeline()
        # results = [pipeline(cv2.imread(file)) for file in all_photos_abs]
        

async def get_photos(timestamp):
    print(timestamp)
    ### IDEALLY
    # os.exec(f"mkdir {os.environ.get('PHOTO_MAIN_FOLDER')}/{timestamp}")
    # for i in range(os.environ.get("CAMERA_AMOUNT"))
        # do photo
        # save_photo(f"{os.environ.get('PHOTO_MAIN_FOLDER')}/{timestamp}/camera_{i}.jpeg")

    ### DEMO
    print('HERE')
    # all_files = [os.path.join(settings.PARENT_ROOT / "testfolder", file) for file in os.listdir(settings.PARENT_ROOT / "testfolder")]
    # random_files = np.random.choice(all_files, size=5, replace=False)

    os.makedirs(f'{os.path.join(settings.MEDIA_ROOT, timestamp)}', exist_ok=True)
    os.system(f'cp /home/sadevans/space/personal/BackWPDD/testfolder/*.jpeg {settings.MEDIA_ROOT}/{timestamp}/')
    