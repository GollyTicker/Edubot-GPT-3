
import openai

with open('.key', 'r') as file:
    openai.api_key = file.read().replace('\n', '')

init_prompt = ""
with open('prompt-edu-chat.txt', 'r') as file:
    init_prompt = file.read()

print("Ask a question or a topic you are interested to learn about: ", end = "")
question = 0
prompt = init_prompt
while question not in [".", ""] :
    question = input()
    prompt = prompt + "\nQ. " + question + "\n "
    response_object = openai.Completion.create(engine="davinci", prompt=prompt, max_tokens=100, temperature = 0.7, stop = "Q. ")
    response = response_object["choices"][0]["text"]
    print(response)
    prompt = prompt + response
