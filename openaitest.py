import os
import openai
from config import apikey

openai.api_key = apikey

response = openai.Completion.create(
  model="gpt-3.5-turbo",
  prompt="write an email to my boss for resignation\n",
  temperature=1,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

print(response)

'''
{
  "warning": "This model version is deprecated. Migrate before January 4, 2024 to avoid disruption of service. Learn more https://platform.openai.com/docs/deprecations",
  "id": "cmpl-80bnTHHx2pKQoWsSWRI9ZALOvl86W",
  "object": "text_completion",
  "created": 1695155983,
  "model": "text-davinci-003",
  "choices": [
    {
      "text": "\nSubject: Resignation - [Your Name]\n\nDear [Boss Name],\n\nThis email serves as notification of my resignation from [Company], effective [date].\n\nI would like to thank you and our colleagues for the opportunity to work with this amazing team, and I have learned a lot from my time here.\n\nI hope we can remain in contact after my departure.\n\nRegards,\n\n[Your Name]",
      "index": 0,
      "logprobs": null,
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 9,
    "completion_tokens": 92,
    "total_tokens": 101
  }
}
'''