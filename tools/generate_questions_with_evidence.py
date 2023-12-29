from openai import OpenAI
import os
import os.path
from dotenv import load_dotenv
from constants import get_integreat_pages_path, get_questions_with_evidence_path, RAW_SLUG, RESPONSES_SLUG

load_dotenv()
client = OpenAI()

prompt = f'''Give three simple and short one-part questions that can be answered with the users message.
The question should be specific and in easy-to-understand language.
Bad examples:
- What services are offered?
- How many people live in Germany?
Respond by giving the questions AND the answers.
For the answers, only give the line numbers, do not give whole sentences.
Good example:
"""
Q1: What language courses are available?
A1: 3, 4, 5
Q2: How can I find language courses?
A2: 7
Q3: What does language level B2 mean?
A3: 6
"""'''


def generate_questions(slug):
    page_path = get_integreat_pages_path(slug)
    raw_path = get_questions_with_evidence_path([RAW_SLUG, slug])
    responses_path = get_questions_with_evidence_path([RESPONSES_SLUG, slug])

    if os.path.isfile(raw_path):
        print(f'Skipping {slug}: Already exists')
        return

    page_file = open(page_path, 'r')
    content = page_file.read()

    if 'The service is free' in content:
        # Questions about pages with specific services are most of the time things like 'Is the service free?'
        print(f'Skipping {slug}: Specific service')
        return

    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'system', 'content': prompt},
            {'role': 'user', 'content': content},
        ]
    )
    print(f'Generated {slug}: {response}')

    raw_file = open(raw_path, 'w')
    raw_file.write(response.choices[0].message.content)

    response_file = open(responses_path, 'w')
    response_file.write(str(response))


if __name__ == '__main__':
    os.makedirs(get_questions_with_evidence_path([RAW_SLUG]), exist_ok=True)
    os.makedirs(get_questions_with_evidence_path([RESPONSES_SLUG]), exist_ok=True)

    page_path = get_integreat_pages_path('')
    slugs = os.listdir(page_path)

    for slug in slugs[:65]:
        generate_questions(slug)
