from contextlib import redirect_stdout

tts_stdout = open("tts-stdout.log", "a")

print("Loading....")
from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer

with redirect_stdout(tts_stdout):
    manager = ModelManager("/models.json")
    model_name = "tts_models/en/ljspeech/tacotron2-DDC"
    # https://github.com/coqui-ai/TTS/blob/dev/TTS/bin/synthesize.py#L286
    model_path, config_path, model_item = manager.download_model(model_name)
    vocoder_name = "vocoder_models/en/ljspeech/hifigan_v2"
    vocoder_path, vocoder_config_path, _ = manager.download_model(vocoder_name)

    # https://github.com/coqui-ai/TTS/blob/f7587fc1346987e2882419ded3dc8b82d12a3b39/TTS/utils/synthesizer.py#L19
    synthesizer = Synthesizer(
        tts_checkpoint=model_path,
        tts_config_path=config_path,
        vocoder_checkpoint=vocoder_path,
        vocoder_config=vocoder_config_path,
    )

print("DONE. ✅")


def convert(text, outpuf_file):
    with redirect_stdout(tts_stdout):
        # https://github.com/coqui-ai/TTS/blob/f7587fc1346987e2882419ded3dc8b82d12a3b39/TTS/utils/synthesizer.py#L174
        wav = synthesizer.tts(text)
    synthesizer.save_wav(wav, outpuf_file)
