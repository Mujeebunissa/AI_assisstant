
apikey2 = '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'

import os
import openai

openai.api_key = apikey2

response = openai.ChatCompletion.create(
    model="text-davinci-003",
    messages='',
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)

print(response)
