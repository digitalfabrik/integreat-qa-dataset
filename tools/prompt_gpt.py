from openai import OpenAI
from dotenv import load_dotenv
from constants import RAW_SLUG, RESPONSES_SLUG, GPT

load_dotenv()
client = OpenAI()


def prompt_gpt(prompt, id, path):
    response = client.chat.completions.create(
        model=GPT,
        messages=[
            {'role': 'system', 'content': prompt},
        ]
    )

    raw_file = open(f'{path}/{RAW_SLUG}/{id}.txt', 'w')
    raw_file.write(response.choices[0].message.content)

    response_file = open(f'{path}/{RESPONSES_SLUG}/{id}.txt', 'w')
    response_file.write(str(response))
