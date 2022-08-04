import os
import sys
import openai

openai.api_key = "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"

def gpt3(prompt_input, maxTokens, temperature):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt_input,
        temperature=temperature,
        max_tokens=maxTokens,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0)
    content = response.choices[0].text.split(".")
    price = 0
    try:
        price = (len(response) / 4000) * 0.06
    except:
        print("Error: Please specify a number for max tokens")
    print("Estimated costs: $", round(price, 4), "max")
    return response.choices[0].text, price

def gpt3_curie(prompt_input, maxTokens, temperature):
    response = openai.Completion.create(
        engine="text-curie-001",
        prompt=prompt_input,
        temperature=temperature,
        max_tokens=maxTokens,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0)
    content = response.choices[0].text.split(".")
    price = 0
    return response.choices[0].text, price

# print("Please specify your input")
# prompt_input = input()
# maxTokens = 500
# temperature = 0.2
#
# print(gpt3(prompt_input, maxTokens, temperature))
