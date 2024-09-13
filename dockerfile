FROM python:3.8-slim

RUN export DEBIAN_FRONTEND=noninteractive && \
    export ACCEPT_EULA=Y && \
    apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y --no-install-recommends \
      curl \
      xcb \ 
      ffmpeg \
      libglib2.0-0 \
      libgl1-mesa-glx && \
    apt-get -y clean && \
    rm -rf /var/lib/apt/lists/*

COPY model/WPDD/model_zoo /opt/operator-server/model/model_zoo

COPY model/WPDD/pallet_processing /opt/operator-server/model/pallet_processing

COPY model/WPDD/requirements.txt /opt/operator-server/model/requirements.txt

COPY model/WPDD/setup.py /opt/operator-server/model/setup.py

WORKDIR /opt/operator-server/model

RUN pip install --no-cache-dir -e .

COPY ./requirements.txt /opt/operator-server

WORKDIR /opt/operator-server

RUN pip install --no-cache-dir -r requirements.txt

COPY wpdd /opt/operator-server/wpdd

WORKDIR /opt/operator-server/model

ARG MODELS_PATH=/opt/operator-server/model/model_zoo

RUN python download_models.py

EXPOSE 8000

CMD ["python", "wpdd/manage.py", "runserver", "0.0.0.0:8000"]