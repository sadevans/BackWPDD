# WPDD System: Wood Pallete Defect Detection System

Система компьютерного зрения для автоматического обнаружения дефектов паллет.

Подробное описание проекта можно найти [тут](https://docs.google.com/document/d/1KbKw75N9EqUMExl1d0_bC0I7z0En-RF6bEThfV5-RJs/edit)

### Цель проекта
Перед разработкой были поставлены следующие цели:

- Снизить нагрузку на специалистов
- Уменьшить аварийность
- Уменьшить срок реагирования на дефектные паллеты
- Снизить затраты на замену дефектных паллет

### Распределение ролей
[Алина](https://github.com/Firally) - `ML engineer`

[Глеб](https://github.com/onoregleb) - `ML engineer`, `Data engineer`

[Юля](https://github.com/YuliaOv22) - `Product Manager`

[Миша](https://github.com/justroflangit) - `Data engineer`

[Саша](https://github.com/sadevans) - `Backend developer`, `Devops`

Алина и Глеб вели разработку в [репозитории модели](https://github.com/sadevans/WPDD).

## Установка
Для начала склонируйте репозиторий:
```shell
git clone https://github.com/sadevans/BackWPDD.git
```

Перейдите в директорию проекта:
```shell
cd BackWPDD
```
Чтобы проиницивализировать сабмодуль модели:
```
git submodule update --init --recursive
```

Для того, чтобы запустить систему, необходимо поднять докер контейнер. Это может занять некоторое время (примерно 10 минут).

```shell
docker compose up -d
```
Теперь загрузились все необходимые библиотеки и пакеты, скачались веса моделей. Система готова к работе.

После этого можно будет перейти на веб-страницу и начать работу.

### Пререквизиты
В скриптах используются следующие переменные среды:
- `YOLO_MODEL_PATH` = 'pallets_plus_defects.pt'
- `BOTTOM_CLASSIF_MODEL_PATH` = 'vit_bottom_v2.pth'
- `SIDE_CLASSIF_MODEL_PATH` = 'vit_side_v2.pth'
- `PACKET_CLASSIF_MODEL_PATH` = 'mobilenet_v2_binary_classification_packet.pth'
- `MODELS_PATH` = './model_zoo/'

Переменные среды можно изменить в docker-compose через .env


## Использование

[Короткая демонстрация работы системы](https://drive.google.com/file/d/1ZA9UE5zi6_PlCiE3s04x5oClytjAvFi7/view?usp=sharing)



Для того, чтобы протестировать систему, необходимо нажать на кнопку `Начать работу`. После ее нажатия откроется WebSocket соединение - сервер, контроллер и вебсокет клиент (имитация конвейера) начнут общаться между собой.

## Разработка

### Используемые интрументы

Разметка данных:
- LabelMe
- CVAT.ai

Бэкенд написан с использованием следующих интрументов:
- Django
- Reddis
- WebSockets
- Vanilla JS
- HTML + CSS

Разработка модели велась Алиной и Глебом в [репозитории модели](https://github.com/sadevans/WPDD). Для разработки использовались:
- PyTorch
- Torchvision
- Ultralitics YOLO
- Transformers
- OpenCV, Pillow

В качестве оркестратора выборан Docker-Compose.

## Используемые датасеты
- [Распознавание дефектов дерева (Large Scale Image Dataset of Wood Surface Defects)](https://www.kaggle.com/datasets/nomihsa965/large-scale-image-dataset-of-wood-surface-defects)

- [Распознавание паллет (pallet detection Computer Vision Project)](https://universe.roboflow.com/sundharesan-kumaresan/pallet-detection-ith6b)
- [Распознавание паллет (Computer Vision Project)]([https://universe.roboflow.com/sundharesan-kumaresan/pallet-detection-ith6b](https://universe.roboflow.com/palette/x-nbtav))
- [Самостоятельно собранный датасет + разметка](https://drive.google.com/drive/folders/1Z_Monpry0OlOtElsb2btXsvmj8nBJ3dB)


## Используемые модели

Весь код моделей можно найти в [этом репозитории](https://github.com/sadevans/WPDD).

- [Модель детекции паллетов и дефектов паллетов [YOLO]](https://drive.google.com/file/d/1XsLvJ6dbJ4yyBbTFzl66V1UQbWQCSlKt/view?usp=sharing)
- [Модель классификации паллетов (в пленке / не в пленке) [MobileNetV2]](https://drive.google.com/file/d/1ZVC8dSctN0Y13qOBmPS7XZXf268Ze-FU/view?usp=sharing)
- [Модель классификации паллетов сбоку (заменить / не заменить) [ViT]](https://drive.google.com/file/d/1US2OXAzxvxiCNdqhHjbYOpCFdihkOqPj/view?usp=sharing)
- [Модель классификации паллетов снизу (заменить / не заменить) [ViT]](https://drive.google.com/file/d/1hRHMrUeWchxfvrNhMT_qEDqU1OLNAlHO/view?usp=sharing)


## Схема разработанной системы
![schema](https://github.com/user-attachments/assets/9cbf4913-8f0a-4ca4-8162-1851ece1a771)

Элементы системы:
- WebSocket клиент
- Сервер - реализован с помощью двух консьюмеров, один общается с веб-страницей, второй с WebSocket клиентом, общение между этими консьюмерами реализовано через Reddis
- Веб-страница
- Камеры К1 и К2 - имитированы засчет копирования фото из тестовой папки
- Конвейер - имитирован засчет задержек после основных команд

Описание общения элементов системы:
1. Паллет приходит по конвейеру в зону камеры К1, конвейер останавливается, отправляет сигнал
2. Сигнал остановки конвейера детектируется сторонним клиентом (реализована имитация детекции)
3. Сторонний клиент отправляет на сервер через WebSocket сигнал, что пора сделать фото на камеру К1
4. Сервер принимает этот сигнал и отправляет сигнал камере К1, камера К1 делает фото (реализована имитация - фото копируются из тестовой папки)
5. Когда фото сделаны, сервер дает самому себе команду выполнить инференс пайплайна классификации паллета на этом фото
6. Выполняется инференс пайплайна классификации паллета, ответ по каждому фото отправляетсся сервером на веб-страницу

    _Также ответ по каждому фото отправляется конвейеру, и если ему приходит после первого фото ответ 1 (паллет годен) - дается сигнал конвейеру отправить паллет в зону камеры К2. Там повторяются шаги 3-5. Если же после первого фото приходит ответ 1 (паллет надо заменить) - отправляется сигнал конвейеру отправить паллет в зону замены._

7. Когда приходит ответ 1 (то есть паллет необходимо заменить) или же когда заинференсены все 5 фото - отправляется ответ по этому паллету на веб страницу, затем отправляется сигнал конвейеру отправить паллет в зону замены. После этого ожидаетсся новый паллет.

    _Если по всему паллету ответ 0 (паллет годен) - отправляется сигнал конвейеру отправить его на слад. После этого ожидается новый паллет._


Описание алгоритма:

1. Проход паллеты по конвейеру + фото снизу камерой К1
2. Обработка фото + принятие решения о замене 
3. Перемещение паллеты на поворотную платформу

    _Если на шаге 2 принято решение о замене, паллета едет в сторону замены, если нет — продолжается процесс детекции_

5. Съемка паллеты камерой К2 с 4-х сторон во время вращения платформы + принятие решения о замене 

    _Фото обрабатываются последовательно, при первом обнаружении дефекта процесс детекции останавливается, паллета едет на замену_

### UML-диаграмма последовательности
Логика общения между различными элементами системы представлена на UML-диаграмме

![uml](https://github.com/user-attachments/assets/cebc4fff-ac22-4932-b516-a1994f6e50e7)


### Файловая архитектура проекта
  ```
  .
  ├── wpdd
  |   ├── wpdd
  |   |   |──core
  |   |   |  |──migrations
  |   |   |  |  └── start_page.css
  |   |   |  |
  |   |   |  |──__init__.py
  |   |   |  |──admin.py
  |   |   |  |──apps.py
  |   |   |  |──consumers.py
  |   |   |  |──models.py
  |   |   |  |──routing.py
  |   |   |  |──tests.py
  |   |   |  |──views.py
  |   |   |
  |   |   |──__init__.py
  |   |   |──asgi.py
  |   |   |──settings.py
  |   |   |──urls.py
  |   |   |──wsgi.py
  |   |
  |   ├── templates
  |   |   └── start_page.html
  |   |
  |   ├── statiс
  |   |   └── assets
  |   |   |   └── start_page.js
  |   |   |
  |   |   └── css
  |   |       └── start_page.css
  |   └── manage.py
  |   └── __init__.py
  |
  ├── fm
  |   ├──consumers.py
  |   ├──dockerfile
  |   ├──requirements.txt
  |
  ├── model
  |   ├──WPDD
  |
  ├── testfolder
  ├──.dockerignore
  ├──.gitignore
  ├──.gitmodules
  ├──README.md
  ├──docker-compose.yml
  ├──dockerfile
  ├──requirements.txt
  ```
Описание элементов файловой системы:
- `wpdd` - директория, в которой структурирован код сервера.
- `wpdd/templates` - html шаблоны.
- `wpdd/static` - js файлы и css файлы.
- `wpdd/wpdd/core` - ключевое приложение django, в нем находятся файлы по умолчанию, необходимые для сборки проекта
- `wpdd/wpdd/core/consumers.py` - взаимодействие сервера с WebSocket-клиентом и веб-страницей
- `wpdd/manage.py` - ключевой файл запуска сервера.
- `fm` - директория, в которой струтктурирован код WebSocket-клиента.
- `fm/consumers.py` - файл, в котором реализован WebSocket-клиент.
- `model` - это сабмодуль, в котором расположен репозиторий [модели](https://github.com/sadevans/WPDD).
- `testfolder` - директория, из которой копируются файлы для демонстрации, имитируя работу камер, в промышленном варианте не нужна.
