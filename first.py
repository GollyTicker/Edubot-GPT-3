import logging
import openai
import init
import details
import json
import copy
import wikipedia

logging.basicConfig(filename='first.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)

with open('.key', 'r') as file:
    openai.api_key = file.read().replace('\n', '')

question = 0
prompts = init.array

gpt3options = {
  "max_tokens": 200,
  "temperature": 0.7,
  "stop": "Q. ",
}

gpt3_details_options = {
  "max_tokens": 2,
  "temperature": 0.7,
}

def main():
    print("Ask a question or a topic you are interested to learn about. (Write . to quit.)")

    while True:
        print("Q. ", end = "")
        question = input()
        if question in [".",""]:
            break

        response = ""
        if question_is_detailed(question):
            topic = extract_topic_of_discussion(prompts) # exclude last question
            summary = get_wikipedia_summary(topic)

            if summary is not None:
                add_wikipedia_summary_to_history(topic, summary, prompts)
            else:
                logging.info("Summary was empty. Not ignoring wikipedia.")

        prompts.append("Q. " + question)
        response = execute_gpt3_request(prompts, gpt3options, "Response")

        # display response
        print(response)
        prompts.append(response)

        # remove oldest question answer pair
        while len(prompts) > 2 * 4:
            prompts.pop(0)
            prompts.pop(0)

        logging.info("Prompts: \n" + '  \n'.join(prompts))

    print("Ended conversation.")

def extract_topic_of_discussion(prompts):
    return "Mars planet"

def add_wikipedia_summary_to_history(topic, summary, prompts):
    prompts.append("Q. What is " + topic+"?")
    prompts.append("E. " + summary)
    logging.info("Prompts after wikipedia: " + '  \n'.join(prompts))

def get_wikipedia_summary(topic):
    try:
        logging.info("Requesting wikipedia for more details on: " + topic)
        result = wikipedia.summary(topic, sentences=7)
        # logging.info("Wikipedia: " + result)
        return result
    except e:
        logging.exception("Encountered an error during wikipedia API for topic:" + topic)
        return None

def question_is_detailed(question):
    request = copy.deepcopy(details.array)
    request.append("Q. " + question)
    response = execute_gpt3_request(request, gpt3_details_options, "Detailed?")
    return response == "Yes"


def execute_gpt3_request(prompts, options, reason):
    response_object = openai.Completion.create(
        engine="davinci",
        prompt=to_multiline_string(prompts),
        **options
    )
    logging.info(reason + f" {json.dumps(response_object,indent=2)}")
    return clean_newlines(response_object["choices"][0]["text"])


def to_multiline_string(prompts):
    return "\n".join(prompts)

def clean_newlines(response):
    if response[:1] == "\n":
        response = response[1:]
    if response[-1:] == "\n":
        response = response[:-1]
    return response

if __name__ == "__main__":
    main()
