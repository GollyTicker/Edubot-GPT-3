import subprocess
import edubot
import simpleaudio as sa
from string_operations import remove_prefix
from itertools import dropwhile

output_sequence = []

# Test prompt: Explain me in detail how a computer works.


def speak_to_user(*args, **kwargs):
    text = args[0]
    lineEnding = kwargs["end"] if "end" in kwargs else "\n"

    print(f"{text}", end=f"{lineEnding}")

    output_sequence.append(text)

    edubot_response_suffix = find_edubot_response_suffix(text)

    if edubot_response_suffix != "":
        print("  >> tts-ing", '"' + edubot_response_suffix + '"')
        convert_to_speech_sequence(edubot_response_suffix)
        print("  >> tts-ing ✅")


def convert_to_speech_sequence(text):
    # convert each line separately, because otherwise the TTS takes too long before the first result
    lines = text.split("\n")

    for i, line in enumerate(lines):
        output_file = f"output/response-{i}.wav"
        subprocess.run(["tts", "--out_path", output_file, "--text", line])


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
