FROM python:3.8-slim

WORKDIR /opt/operator-server

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

COPY ./requirements.txt /opt/operator-server

RUN pip install -r requirements.txt

COPY wpdd /opt/operator-server/wpdd

EXPOSE 8000

CMD ["python", "wpdd/manage.py", "runserver", "0.0.0.0:8000"]