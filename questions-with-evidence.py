from openai import OpenAI
import os
import os.path
from dotenv import load_dotenv

CHARS_PER_ANSWER = 500
MAX_ANSWERS = 3

load_dotenv()
client = OpenAI()


def number_answers(content):
    answers = 1 + len(content) / CHARS_PER_ANSWER
    return int(min(answers, MAX_ANSWERS))


def get_pages_data_path(city, language, slug):
    return f'data/integreat-pages/{city}/{language}/pages/{slug}'


def get_data_path(city, language, slugs):
    return f'data/gpt-with-evidence/{city}/{language}/{"/".join(slugs)}'


def create_answers(city, language, slug):
    page_path = get_pages_data_path(city, language, f'{slug}.txt')
    answer_path = get_data_path(city, language, ['answers', f'{slug}.txt'])
    raw_path = get_data_path(city, language, ['raw', f'{slug}.txt'])

    if os.path.isfile(answer_path):
        # Skip pages with already existing answers
        return

    page_file = open(page_path, 'r')
    content = page_file.read()

    prompt = f'''Give three simple and short one-part questions that can be answered with the users message.
The question should be specific and in easy-to-understand language.
Bad examples:
- What services are offered?
- How many people live in Germany?
Respond by giving the questions AND the answers (ONLY the line numbers).
Good example:
"""
Q1: What language courses are available?
A1: 3, 4, 5
Q2: How can I find language courses?
A2: 7
Q3: What does language level B2 mean?
A3: 6
"""'''

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": content},
        ]
    )
    print(response)

    answer_file = open(answer_path, 'w')
    answer_file.write(response.choices[0].message.content)

    raw_file = open(raw_path, 'w')
    raw_file.write(str(response))


CITY = 'muenchen'
LANGUAGE = 'en'


# Ideas:
# - Use multiple user messages, one each for each content
# - Add multiple paragraphs in one message

# TODOs:
# - Fix answer sentence numbers
# - Postprocess answers
if __name__ == '__main__':
    os.makedirs(get_data_path(CITY, LANGUAGE, ['answers']), exist_ok=True)
    os.makedirs(get_data_path(CITY, LANGUAGE, ['raw']), exist_ok=True)

    page_path = get_pages_data_path(CITY, LANGUAGE, '')
    slugs = os.listdir(page_path)

    # slugs = ['268453', '277673', '264450']
    for slug in slugs[:5]:
        create_answers(CITY, LANGUAGE, slug[:slug.index('.txt')])
