from openai import OpenAI
import os
import os.path
from dotenv import load_dotenv
from constants import get_integreat_pages_path, get_questions_with_evidence_path, RAW_SLUG, RESPONSES_SLUG, LANGUAGE

load_dotenv()
client = OpenAI()

prompt_en = f'''Give three simple and short one-part questions that can be answered with the users message.
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

prompt_de = f'''Give three simple and short one-part questions that can be answered with the users message.
The question should be specific and in easy-to-understand German language.
Bad examples:
- Welche Dienstleistungen werden angeboten?
- Wie viele Menschen leben in Deutschland?
Respond by giving the questions AND the answers.
For the answers, only give the line numbers, do not give whole sentences.
Good example:
"""
Q1: Welche Sprachkurse gibt es?
A1: 3, 4, 5
Q2: Wie kann ich Sprachkurse finden?
A2: 7
Q3: Was bedeutet das Sprachniveau B2?
A3: 6
"""'''


# Add line numbers to each line
def enumerate_lines(text):
    lines = text.split('\n')
    numerated_lines = []
    for index, line in enumerate(lines):
        numerated_lines.append(str(index) + ' ' + line)

    return '\n'.join(numerated_lines)


def generate_questions(slug):
    page_path = get_integreat_pages_path(slug)
    raw_path = get_questions_with_evidence_path([RAW_SLUG, slug])
    responses_path = get_questions_with_evidence_path([RESPONSES_SLUG, slug])

    if os.path.isfile(raw_path):
        print(f'Skipping {slug}: Already exists')
        return

    page_file = open(page_path, 'r')
    content = page_file.read()

    if ('The service is free' in content) or ('Das Angebot ist kostenfrei' in content):
        # Questions about pages with specific services are most of the time things like 'Is the service free?'
        print(f'Skipping {slug}: Specific service')
        return

    if len(content) > 5000:
        # Max context length in the backend is 5000 chars
        print(f'Skipping {slug}: Context too long')
        return

    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'system', 'content': prompt_de if LANGUAGE == 'de' else prompt_en},
            {'role': 'user', 'content': enumerate_lines(content)},
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
