from pathlib import Path
import os
import edubot
import simpleaudio as sa
from string_operations import remove_prefix
from itertools import dropwhile
from pathlib import Path
import text_to_speech

# Test prompt: Explain me in very detail how a computer works.


def speak_to_user(*args, **kwargs):
    text = args[0]
    lineEnding = kwargs["end"] if "end" in kwargs else "\n"

    print(f"{text}", end=f"{lineEnding}")

    edubot_response_suffix = find_edubot_response_suffix(text)

    if edubot_response_suffix != "":
        convert_to_speech_sequence(edubot_response_suffix)


def convert_to_speech_sequence(text):
    # convert each line separately, because otherwise the TTS takes too long before the first result
    lines = text.split("\n")

    os.system("rm -f output/response-*.wav")
    for i, line in enumerate(lines):
        print("  >> tts-ing", '"' + line + '"')
        text_to_speech.convert(line, f"output/response-{i}.wav")

    print("  >> tts-ing ✅")


# find everything after the "E. " in the textual response
def find_edubot_response_suffix(text):
    lines = text.split("\n")

    def is_before_edubot_response(line):
        return not line.startswith(edubot.EXPLANATION_PREFIX)

    edubot_response_lines = list(dropwhile(is_before_edubot_response, lines))

    # remove "E. " from the edubot response lines.
    if len(edubot_response_lines) != 0:
        edubot_response_lines[0] = remove_prefix(
            edubot.EXPLANATION_PREFIX, edubot_response_lines[0]
        )

    return "\n".join(edubot_response_lines)


edubot.main(printer=speak_to_user, inputter=input)
