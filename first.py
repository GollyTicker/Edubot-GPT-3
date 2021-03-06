import logging
import openai
import init
import details
import json
import copy

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

def to_multiline_string(prompts):
    return "\n".join(prompts)

def clean_newlines(response):
    if response[:1] == "\n":
        response = response[1:]
    if response[-1:] == "\n":
        response = response[:-1]
    return response

def question_is_detailed(question):
    request = copy.deepcopy(details.array)
    request.append("Q. " + question)
    response = execute_gpt3_request(request, gpt3_details_options, "Detailed?")
    logging.info("Request wikipedia for more details? -> " + str(response == "Yes"))
    return response == "Yes"

def execute_gpt3_request(prompts, options, reason):
    response_object = openai.Completion.create(
        engine="davinci",
        prompt=to_multiline_string(prompts),
        **options
    )
    logging.info(reason + f" {json.dumps(response_object,indent=2)}")
    return clean_newlines(response_object["choices"][0]["text"])

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
        response = execute_gpt3_request(prompts, gpt3options, "Response") # "E. <some wikipedia enhanced response>"
    else:
        response = execute_gpt3_request(prompts, gpt3options, "Response")

    # display response
    print(response)
    prompts.append(response)

    # remove oldest question answer pair
    if len(prompts) > 2 * 4:
        prompts.pop(0)
        prompts.pop(0)

    logging.info("Prompts: \n" + '  \n'.join(prompts))

print("Ended conversation.")
