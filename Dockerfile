FROM python:3.8
RUN apt update && apt install -y libsndfile-dev
WORKDIR /app
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
#work in progress debugging.
RUN apt-get update && apt-get install -y python3-dev libasound2-dev portaudio19-dev python3-all-dev pulseaudio && pip3 install pyaudio simpleaudio
COPY docker-setup* ./
RUN bash docker*.sh
RUN ls -lah
CMD bash