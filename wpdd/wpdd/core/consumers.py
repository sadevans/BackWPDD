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
from pallet_processing.pipeline import InferencePipeline
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
        text_data_json = json.loads(text_data)
        if text_data_json['type'] == 'success':
            pass

        elif text_data_json['type'] == 'get_new_pallete':
            print('IM HERE IN NEW PALLETE ARRIVED')

            timestamp = text_data_json['pallete_id']
            await self.channel_layer.group_send(
                'file_watch_group',
                {
                    'type': 'new_pallete',
                    'timestamp': timestamp,
                }
            )

        elif text_data_json['type'] == 'camera':
        # elif text_data_json['type'] == 'camera1':
            timestamp = text_data_json['pallete_id']

            # if text_data_json['camera_id'] == 1

            name = await get_one_photo(timestamp) if text_data_json['camera_id'] == 1 else await get_four_photos(timestamp)
            # name = await get_one_photo(timestamp) # имитация съемки камеры №1 (дно паллета)
            # camera_id = 1

        # elif text_data_json['type'] == 'camera2':
        #     # timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        #     timestamp = text_data_json['pallete_id']
        #     name = await get_four_photos(timestamp) # имитация съемки камеры №2 (фото сбоку)
        #     camera_id = 2

            # Send a message to the 'file_watch_group'
            # await asyncio.gather(
            await self.channel_layer.group_send(
                'file_watch_group',
                {
                    'type': 'camera_done',
                    'timestamp': timestamp,
                    'name': name,
                    'camera_id': text_data_json['camera_id'],
                    'num_photos': len(name)
                }
            )
            
            # await self.channel_layer.group_send(
            #     'file_watch_group',
            #     {
            #         'type': 'models_inference',
            #         'timestamp': timestamp,
            #         'name': name,
            #         'camera_id': text_data_json['camera_id']
            #     }
            # )
            # )

    async def new_pallete(self, event):
        pass

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
        await self.send(text_data=json.dumps({
                        'type': 'model_responce',
                        'answer': event['answer'],
                        'camera_id': event['camera_id'],
                        'photo_id': event['photo_id']
                    }))


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        await self.channel_layer.group_add(
            'file_watch_group',
            self.channel_name
        )
        await self.accept()
        self.pipeline = InferencePipeline()


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

        await self.channel_layer.group_send(
            'file_watch_group',
            {
                'type': 'front_init'
            }
        )


    async def front_init(self, event):
        pass


    async def new_pallete(self, event):
        await self.send(text_data=json.dumps({
                    'type': 'new_pallete_arrived',
                    # 'camera_id': event['camera_id'],
                    # 'num_photos': event['num_photos'],
                    'message': f"New pallete with ID={event['timestamp']} has arived !",
                    # 'images': encoded_photos_list,
                    'pallete_id': event['timestamp']
                }))


    async def camera_done(self, event):
        # считывание сделанных камерой фото, отправка их на фронт
        timestamp = event['timestamp']
        print(f"Received pallete: {timestamp}")
        await self.send(text_data=json.dumps({
                    'type': 'camera_done',
                    'camera_id': event['camera_id'],
                    'num_photos': event['num_photos'],
                    # 'images': encoded_photos_list,
                    'pallete_id': timestamp
                }))
        
        await self.channel_layer.group_send(
                'file_watch_group',
                {
                    'type': 'models_inference',
                    'timestamp': timestamp,
                    'name': event['name'],
                    'camera_id': event['camera_id']
                }
        )
        

        

    async def models_inference(self, event):
        # запуск инференса модели
        timestamp = event['timestamp']
        name_photo = event['name']
        camera_id = event['camera_id']

        all_photos_abs = []
        encoded_photos = []
        for i, photo in enumerate(name_photo):
            print(i, photo)
            try:
                photo_path = os.path.join(f"{settings.MEDIA_ROOT}/{timestamp}", photo) # абсолютный путь фотографии, лучше поменять
                all_photos_abs.append(photo_path) 

                output = self.pipeline.get_prediction(photo_path)
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ", output)
                answer = int(output['replace_pallet'])

                # считывание данных для фронта - должны считывать выход модели
                in_data_bytes = open(photo_path, "rb").read() # читаем фото для фронта

                # кодирование фото для фронта
                if in_data_bytes:
                    encoded_photo_in = base64.b64encode(in_data_bytes).decode('ascii')
                    encoded_photos.append(encoded_photo_in)

                # реальный номер фото в зависимости от номера камеры (на камеру1 1ое фото, на камеру2 - фото со 2го по 5ое)
                if camera_id == 2:
                    num = i+1
                else:
                    num = i

                # это если в JS отправлять ответ
                print(f"Full Inference Pipeline on photo №{num+1} has been done! ANSWER = {answer}")

                answer_text = 'Defect' if answer == 1 else 'OK'

                await self.send(text_data=json.dumps({
                    'type': 'pipeline_log',
                    # 'message': f"Full Inference Pipeline on photo №{num+1} has been done!\nPhoto №{num+1} is {'Defect' if answer == 1 else 'OK'}",
                    'message': f"Full Inference Pipeline on photo №{num+1} has been done!  ANSWER = {answer}",
                    'answer': answer,
                    'answer_text': answer_text,
                    'photo_id': i+1 if camera_id==1 else i+2,
                    'images': [encoded_photo_in]
                    # 'camera_id': camera_id
                }))
                # отправка ответа контроллеру
                if answer == 1:
                    break

            except Exception as e:
                self.send(text_data=json.dumps({
                    'error': str(e)
                }))

        # if camera_id == 2:
        #     i = i + 1
        # answer_text = 'Defect' if answer == 1 else 'OK'
        await self.channel_layer.group_send(
                    'file_watch_group',
                    {
                        'type': 'pipeline_answer',
                        'timestamp': timestamp,
                        'answer': answer_text,
                        'camera_id': camera_id,
                        'photo_id': num+1,
                        'encoded_photos': [encoded_photo_in],
                        'pallete_id': timestamp
                    }
                )



    async def pipeline_answer(self, event):
        # pass
        await self.send(text_data=json.dumps({
                    'type': 'pipeline_send_answer',

                    'answer': event['answer'],
                    'message': f"Pallete №{event['pallete_id']} is {event['answer']}, answer on photo №{event['photo_id']}",
                    'images': event['encoded_photos'],
                    'photo_id': event['photo_id'],
                    'pallete_id': event['pallete_id']
                    # 'answer': answer,
                    # 'camera_id': camera_id
                }))




            



            




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
    os.system(f'cp {settings.FAKE_DATA_ROOT}/*.jpeg {settings.MEDIA_ROOT}/{timestamp}/')




async def get_one_photo(timestamp):
    print('HERE IS TAKING ONE PHOTO')
    os.makedirs(f'{os.path.join(settings.MEDIA_ROOT, timestamp)}', exist_ok=True)
    name = os.listdir(f'{settings.FAKE_DATA_ROOT}/one_photo/')
    os.system(f'cp {settings.FAKE_DATA_ROOT}/one_photo/*.jpeg {settings.MEDIA_ROOT}/{timestamp}/')

    return name


async def get_four_photos(timestamp):
    print('HERE IS TAKING FOUR PHOTOs')
    os.makedirs(f'{os.path.join(settings.MEDIA_ROOT, timestamp)}', exist_ok=True)
    names = os.listdir(f'{settings.FAKE_DATA_ROOT}/four_photos/')
    # name_photo = os.listdir()
    os.system(f'cp {settings.FAKE_DATA_ROOT}/four_photos/*.jpeg {settings.MEDIA_ROOT}/{timestamp}/')
    return names
