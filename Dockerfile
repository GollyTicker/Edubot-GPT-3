FROM python:3.8
RUN apt update && apt install -y libsndfile-dev
WORKDIR /app
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
#work in progress debugging.
RUN apt-get update && apt-get install -y python3-dev libasound2-dev portaudio19-dev python3-all-dev pulseaudio && pip3 install pyaudio simpleaudio
RUN apt-get update && apt-get install -y curl && curl -s -o /models.json https://raw.githubusercontent.com/coqui-ai/TTS/dev/TTS/.models.json 
COPY docker-setup-once-initially.sh ./
RUN bash docker-setup-once-initially.sh
RUN ls -lah
CMD bash
