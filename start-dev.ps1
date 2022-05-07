#!/usr/bin/env pwsh

$ErrorActionPreference = "Stop"

docker build -t edubot:v1 .

sh -c "getent group audio | cut -d: -f3 > tmp.log"

$AUDIO_GROUP=type tmp.log

# work in progress debugging...
docker run -it `
  --device /dev/snd `
  -e PULSE_SERVER=unix:${XDG_RUNTIME_DIR}/pulse/native `
  -v ${XDG_RUNTIME_DIR}/pulse/native:${XDG_RUNTIME_DIR}/pulse/native `
  -v ~/.config/pulse:/root/.config/pulse `
  -v /run/dbus/:/run/dbus/ -v /dev/shm:/dev/shm `
  --group-add ${AUDIO_GROUP} `
  -v ${PWD}:/app `
  edubot:v1 python3 speech-edubot.py
