set -e
# ensure, that the docker container downloads the necessary model, so that we can adapt it's config
tts --text "Hello World!"
rm tts*.wav
sed -i 's/{/{"max_decoder_steps": 7000,/g' ~/.local/share/tts/tts_models--en--ljspeech--tacotron2-DDC/config.json
