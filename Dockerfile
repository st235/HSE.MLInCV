FROM python:3.9-slim-bullseye

WORKDIR /web_demo

RUN apt-get update \
    && apt-get install ffmpeg libsm6 libxext6 -y

COPY ./src ./src
COPY ./web_demo.py ./web_demo.py
COPY ./lite-requirements.txt ./lite-requirements.txt

RUN pip3 install -r lite-requirements.txt

CMD [ "streamlit", "run", "web_demo.py", "--server.port", "8000", "--browser.serverAddress", "0.0.0.0" ]
