# WPDD System: Wood Pallete Defect Detection System

Система компьютерного зрения для автоматического обнаружения дефектов паллет.

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


## Установка
Для начала склонируйте репозиторий:
```shell
git clone https://github.com/sadevans/BackWPDD.git
```

Перейдите в директорию проекта:
```shell
cd BackWPDD
```

Для того, чтобы запустить систему, необходимо поднять докер контейнер. Это может занять некоторое время (примерно 10 минут).

```shell
docker compose up -d
```
Теперь загрузились все необходимые библиотеки и пакеты, скачались веса моделей. Система готова к работе.

После этого можно будет перейти на веб-страницу по адресу ВПИСАТЬ АДРЕС и начать работу.

### Пререквизиты
В скриптах используются следующие переменные среды:
- `YOLO_MODEL_PATH` = 'pallets_plus_defects.pt'
- `BOTTOM_CLASSIF_MODEL_PATH` = 'vit_bottom_v2.pth'
- `SIDE_CLASSIF_MODEL_PATH` = 'vit_side_v2.pth'
- `PACKET_CLASSIF_MODEL_PATH` = 'mobilenet_v2_binary_classification_packet.pth'
- `MODELS_PATH` = './model_zoo/'

Переменные среды можно изменить в docker-compose через .env


## Использование

Короткая демонстрация работы системы:



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

Разработка модели велась Алиной и Глебом в [репозитории модели](https://github.com/sadevans/WPDD)/. Для разработки использовались:
- PyTorch
- Torchvision
- Ultralitics YOLO
- Transformers
- OpenCV, Pillow

В качестве оркестратора выборан Docker-Compose.


## Схема разработанной системы
![conveyor-cameras-inference drawio (1)](https://github.com/user-attachments/assets/e34cfd73-7bbe-4a4e-b32f-9987b3e4f478)

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



###

