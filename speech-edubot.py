import subprocess
import edubot
import simpleaudio as sa


def speak_to_user(*args, **kwargs):
    print(*args, **kwargs)

    source_text = edubot.remove_prefix("Q.", args[0].strip())
    source_text = edubot.remove_prefix("E.", source_text.strip())
    source_text = source_text.strip()

    if source_text != "":
        print("tts-ing: ", source_text)
        speech_file = "tmp.wav"
        subprocess.run(["tts", "--out_path", speech_file, "--text", source_text])
        print("Produced speech output. Attempting to play speech audio.")

        # work in progress.... this fails here...
        wave_obj = sa.WaveObject.from_wave_file(speech_file)
        play_obj = wave_obj.play()
        play_obj.wait_done()


edubot.main(printer=speak_to_user, inputter=input)
