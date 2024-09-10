import base64
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.files import File
from django.core.files.storage import default_storage
from django.conf import settings
from datetime import datetime
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import os
import cv2
import numpy as np
import shutil
import subprocess
import random
import asyncio
# from pipelines.pipelines import DetectDefectsPipeline




class ControlConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Connect to a group called 'file_watch_group'
        await self.channel_layer.group_add(
            'file_watch_group',
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Remove from the group on disconnect
        await self.channel_layer.group_discard(
            'file_watch_group',
            self.channel_name
        )

    async def receive(self, text_data):
        print('HERE WE GO AGAIN')
        text_data_json = json.loads(text_data)

        if text_data_json['type'] == 'camera1':
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            name = await get_one_photo(timestamp)
            camera_id = 1

        elif text_data_json['type'] == 'camera2':
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            name = await get_one_photo(timestamp) # имитация съемки камеры №1 (дно паллета)
            camera_id = 2

        # Send a message to the 'file_watch_group'
        await asyncio.gather(
            self.channel_layer.group_send(
                'file_watch_group',
                {
                    'type': 'camera_done',
                    'timestamp': timestamp,
                    'name': name
                }
            ),
            self.channel_layer.group_send(
                'file_watch_group',
                {
                    'type': 'models_inference',
                    'timestamp': timestamp,
                    'name': name,
                    'camera_id': camera_id
                }
            )
        )

        # await self.channel_layer.group_send(
        #     'file_watch_group',
        #     {
        #         'type': 'camera_done',
        #         'timestamp': timestamp,
        #         'name': name
        #     }
        # )

        # await self.channel_layer.group_send(
        #     'file_watch_group',
        #     {
        #         'type': 'models_inference',
        #         'timestamp': timestamp,
        #         'name': name
        #     }
        # )

    async def models_inference(self, event):
        pass


    async def camera_done(self, event):
        pass


    async def front_init(self, event):
        await self.send(text_data=json.dumps({
                        'type': 'front_init',
                        'message': 'Initialize frontend'
                    }))
        

    async def pipeline_answer(self, event):
        print('IM IN PIPELINE ANSWER')
        answ = event['answer']
        timestamp = event['timestamp']
        camera_id = event['camera_id']
        print(f'Received answer = {answ}, timestamp = {timestamp}, camera_id = {camera_id}') # сюда заходит,все ок

        if answ == 0:
            await self.send(text_data=json.dumps({
                            'type': 'model_responce',
                            'answer': 'OK',
                            'camera_id': camera_id
                        }))
        elif answ == 1:
            await self.send(text_data=json.dumps({
                            'type': 'model_responce',
                            'answer': 'Defect',
                            'camera_id': camera_id
                        }))

        

        # if answ == 1:


        # pass




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
        print("here!!!!!")
        await self.send(text_data=json.dumps({
            'message': 'Success'
        }))

        await self.channel_layer.group_send(
            'file_watch_group',
            {
                'type': 'front_init'
            }
        )


    async def front_init(self, event):
        pass


    async def camera_done(self, event):
        print('IM IN CAMERA_DONE: ', datetime.now())
        # считывание сделанных камерой фото, отправка их на фронт
        timestamp = event['timestamp']
        name_photo = event['name']

        print(f"Received timestamp: {timestamp}, photo name: {name_photo}")

        all_photos_abs = []
        encoded_photos_list = []

        # считываем фото и отправляем на фронт их изначальный вид (возможно это не нужно)
        for photo in name_photo:
            try:
                photo_path = os.path.join(f"{settings.MEDIA_ROOT}/{timestamp}", photo) # абсолютный путь фотографии, лучше поменять
                all_photos_abs.append(photo_path) 

                in_data_bytes = open(photo_path, "rb").read() # читаем фото для фронта

                # кодирование фото для фронта
                if in_data_bytes:
                    encoded_photo_in = base64.b64encode(in_data_bytes).decode('ascii')
                    encoded_photos_list.append(encoded_photo_in)
                
                await self.send(text_data=json.dumps({
                    'timestamp': timestamp,
                    'photos': encoded_photos_list
                }))
            
            except Exception as e:
                await self.send(text_data=json.dumps({
                    'error': str(e)
                }))
            print("definetely not here")


        # отправляем фото на фронт
        if len(encoded_photos_list) > 0 :
            print('LEN > 0')
            await self.send(text_data=json.dumps({
                    'type': 'image_batch',
                    'message': 'Success',
                    'images': encoded_photos_list
                }))
            

            # await self.channel_layer.group_send(
            # 'file_watch_group',
            # {
            #     'type': ''
            # }
        # ) 


        else:
            await self.send(text_data=json.dumps({
                'error': 'Unable to read images'
            }))
        print("definetely not here")



    async def models_inference(self, event):
        # запуск инференса модели
        print('IM IN INFERENCE: ', datetime.now())
        timestamp = event['timestamp']
        name_photo = event['name']
        camera_id = event['camera_id']
        for i, photo in enumerate(name_photo):
            print(i, photo)
            try:
                photo_path = os.path.join(f"{settings.MEDIA_ROOT}/{timestamp}", photo) # абсолютный путь фотографии, лучше поменять
                # all_photos_abs.append(photo_path) 
                # answer = IfDefectPalletePipeline(photo_path)
                answer = random.choice([0,1])
                # answer = 0
                print(f'MY ANSWER IS {answer}') # вот до сюда работает !!!

                # это если в JS отпарвлять ответ
                await self.send(text_data=json.dumps({
                    'type': 'pipeline_answer',
                    'timestamp': timestamp,
                    # 'photos': encoded_photos_list
                    'answer': answer,
                    'camera_id': camera_id
                }))

                # отправка ответа контроллеру
                if answer == 0: 
                    break

            except Exception as e:
                await self.send(text_data=json.dumps({
                    'error': str(e)
                }))
        await self.channel_layer.group_send(
                    'file_watch_group',
                    {
                        'type': 'pipeline_answer',
                        'timestamp': timestamp,
                        'answer': answer,
                        'camera_id': camera_id
                    }
                )



    async def pipeline_answer(self, event):
        pass
            



            




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




async def get_one_photo(timestamp):
    print('HERE IS TAKING ONE PHOTO')
    os.makedirs(f'{os.path.join(settings.MEDIA_ROOT, timestamp)}', exist_ok=True)
    name = os.listdir('/home/sadevans/space/personal/BackWPDD/testfolder/one_photo/')
    os.system(f'cp /home/sadevans/space/personal/BackWPDD/testfolder/one_photo/*.jpeg {settings.MEDIA_ROOT}/{timestamp}/')

    return name


async def get_four_photos(timestamp):
    print('HERE IS TAKING FOUR PHOTOs')
    os.makedirs(f'{os.path.join(settings.MEDIA_ROOT, timestamp)}', exist_ok=True)
    names = os.listdir('/home/sadevans/space/personal/BackWPDD/testfolder/four_photos/')
    # name_photo = os.listdir()
    os.system(f'cp /home/sadevans/space/personal/BackWPDD/testfolder/four_photos/*.jpeg {settings.MEDIA_ROOT}/{timestamp}/')
    return names
