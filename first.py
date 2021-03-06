import logging
import openai
from init import init
import json

logging.basicConfig(filename='first.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)

with open('.key', 'r') as file:
    openai.api_key = file.read().replace('\n', '')

question = 0
prompts = init

gpt3options = {
  "max_tokens": 200,
  "temperature": 0.7,
  "stop": "Q. ",
}

def to_multiline_string(prompts):
    return "\n".join(prompts)

def clean_newlines(response):
    if response[:1] == "\n":
        response = response[1:]
    if response[-1:] == "\n":
        response = response[:-1]
    return response

def question_is_detailed(question):
    return False

print("Ask a question or a topic you are interested to learn about. (Write . to quit.)")
while True:
    print("Q. ", end = "")
    question = input()
    if question in [".",""]:
        break
    prompts.append("Q. " + question)

    response = ""
    if question_is_detailed(question):
        # do wikipedia stuff....
        response = "some response"

    else:
        response_object = openai.Completion.create(engine="davinci", prompt=to_multiline_string(prompts), **gpt3options)

        logging.info(f"Response: {json.dumps(response_object,indent=2)}")

        response = clean_newlines(response_object["choices"][0]["text"])

    # display response
    print(response)
    prompts.append(response)

    # remove oldest question answer pair
    if len(prompts) > 2 * 4:
        prompts.pop(0)
        prompts.pop(0)

    logging.info("Prompts: \n" + '  \n'.join(prompts))

print("Ended conversation.")
