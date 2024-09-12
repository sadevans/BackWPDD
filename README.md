<img src="./images/logo.sample.png" alt="Logo of the project" align="right">

# WPDD System: Wood Pallete Defect Detection System

Система компьютерного зрения для автоматического обнаружения дефектов паллет.

### Цель проекта
Перед разработкой были поставлены следующие цели:

- Снизить нагрузку на специалистов
- Уменьшить аварийность
- Уменьшить срок реагирования на дефектные паллеты
- Снизить затраты на замену дефектных паллет

### Требования

Функциональные:
- Детектирование дефекта деревянных паллет с грузом по фотографиям
- Использование алгоритма на основе компьютерного зрения (ИИ)
- Создание алгоритма дообучения модели
- Разработка API для работы с системой, которая возвращает результат: заменить / не заменить паллету

Нефункциональные:
- Время инференса — не более 2 секунд на одну паллету
- Модель должна работать на моделях видеокарты: RTX 3090 / 4090
- Обучение производится на самостоятельно собранных датасетах
- Разметка данных производится самостоятельно
- Учесть, что пропуск поврежденной паллеты критичнее, чем замена хорошей паллеты

### Распределение ролей
[Алина](https://github.com/Firally) - `ML engineer`

[Глеб](https://github.com/onoregleb) - `ML engineer`, `Data engineer`

[Юля](https://github.com/YuliaOv22) - `Product Manager`

[Миша](https://github.com/justroflangit) - `Data engineer`

[Саша](https://github.com/sadevans) - `Backend developer`, `Devops`


## Установка

Для того, чтобы запустить систему, необходимо поднять докер контейнер:

If your project needs some additional steps for the developer to build the
project after some code changes, state them here. for example:

```shell
./configure
make
make install
```

После этого можно будет перейти на веб-страницу по адресу: ВПИСАТЬ АДРЕС

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

