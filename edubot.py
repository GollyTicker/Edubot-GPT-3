import logging
import openai
import init
import details
import json
import copy
import wikipedia

MAXIMUM_NUMBER_OF_QUESTION_ANSWER_PAIRS = 4

logging.basicConfig(
    filename="first.log",
    filemode="w",
    format="%(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

with open(".key", "r") as file:
    openai.api_key = file.read().replace("\n", "")

question = 0
prompts = init.array

gpt3options = {
    "max_tokens": 600,
    "temperature": 0.7,
    "stop": "Q. ",
}

gpt3_details_options = {
    "max_tokens": 2,
    "temperature": 0.95,
}

gpt3_topic_extraction = {
    "max_tokens": 20,
    "temperature": 0.7,
    "stop": "Q. ",
}


def main(printer=print, inputter=input):
    printer(
        "Ask a question or a topic you are interested to learn about. (Write dot '.' or say 'quit' to quit.)"
    )

    while True:
        printer("Q. ", end="")
        question = inputter()
        printer("")
        if question in [".", ""]:
            break

        response = ""
        if question_is_detailed(question):
            topic = extract_topic_of_discussion(prompts)
            summary = get_wikipedia_summary(topic)

            if summary is not None:
                add_wikipedia_summary_to_history(topic, summary, prompts)
            else:
                logging.info("No summary could be found. Ignoring wikipedia.")

        prompts.append("Q. " + question)
        response = execute_gpt3_request(prompts, gpt3options, "Response")

        # display response
        printer(response, end="\n\n")
        prompts.append(response)

        ensure_history_is_truncated(prompts)

        logging.info("Prompts: \n" + "  \n".join(prompts))

    printer("Ended conversation.")


def ensure_history_is_truncated(prompts):
    while len(prompts) > 2 * MAXIMUM_NUMBER_OF_QUESTION_ANSWER_PAIRS:
        prompts.pop(0)
        prompts.pop(0)


def extract_topic_of_discussion(prompts):
    request = copy.deepcopy(prompts)
    request.append("Q. What is the wikipedia page on this topic called?")
    response = execute_gpt3_request(request, gpt3_topic_extraction, "Extracted Topic: ")
    return extract_topic_from_response(response)


def extract_topic_from_response(response):
    logging.info("Extracting topic from " + response)
    response = remove_prefix("E. ", response)
    response = remove_suffix(".", response)
    logging.info("Using extracted topic: " + response)
    return response


def remove_prefix(prefix, response):
    if response[: len(prefix)] == prefix:
        return response[len(prefix) :]
    else:
        return response


def remove_suffix(suffix, response):
    if response[-len(suffix) :] == suffix:
        return response[: -len(suffix)]
    else:
        return response


def add_wikipedia_summary_to_history(topic, summary, prompts):
    prompts.append("Q. What is " + topic + "?")
    prompts.append("E. " + summary)
    logging.info("Prompts after wikipedia: " + "  \n".join(prompts))


def get_wikipedia_summary(topic):
    try:
        logging.info("Requesting wikipedia for more details on: " + topic)
        result = wikipedia.summary(topic, sentences=5)
        return result
    except:
        logging.exception(
            "Encountered an error during wikipedia API for topic:" + topic
        )
        return None


def question_is_detailed(question):
    request = copy.deepcopy(details.array)
    request.append("Q. " + question)
    response = execute_gpt3_request(request, gpt3_details_options, "Detailed?")
    return response == "Yes"


def execute_gpt3_request(prompts, options, reason):
    response_object = openai.Completion.create(
        engine="davinci", prompt=to_multiline_string(prompts), **options
    )
    logging.info(reason + f" {json.dumps(response_object,indent=2)}")
    return clean_newlines(response_object["choices"][0]["text"])


def to_multiline_string(prompts):
    return "\n".join(prompts)


def clean_newlines(response):
    response = remove_prefix("\n", response)
    response = remove_suffix("\n", response)
    return response


if __name__ == "__main__":
    main()

todos = """
TODOs:
. clean rough edges:
    . Q. Can you tell me more about it? -> continues at a random place, because invisible question from wikipedia is appended to history.
    . Make sure only the wikipedia summary is used - while at the same time having a limit on the number of tokens used at input for gpt
    . when the past few questions answers get too long -> shorten them appropiately
    . investigate using cheaper weaker faster engines (curie, ... , ada) instead
. visibility
    . add simple web-interface that is only partially availible
. improvements
"""
