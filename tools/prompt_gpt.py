import os

from openai import OpenAI
from dotenv import load_dotenv
from constants import RAW_SLUG, RESPONSES_SLUG, GPT

load_dotenv()
client = OpenAI()


def prompt_gpt(prompt, id, path):
    raw_path = f'{path}/{RAW_SLUG}/{id}.txt'
    if os.path.isfile(raw_path):
        # Skip pages which already have generated questions
        print(f'Skipping {id}: Already exists')
        return

    response = client.chat.completions.create(
        model=GPT,
        messages=[
            {'role': 'system', 'content': prompt},
        ]
    )

    raw_file = open(raw_path, 'w')
    raw_file.write(response.choices[0].message.content)

    response_file = open(f'{path}/{RESPONSES_SLUG}/{id}.txt', 'w')
    response_file.write(str(response))
