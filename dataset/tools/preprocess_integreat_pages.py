import os
import requests
import json
import re
from bs4 import BeautifulSoup
from constants import get_integreat_pages_path, get_integreat_pages_json_path, CITY, LANGUAGE
from tools.postprocess_with_context import postprocess

MIN_CONTENT_LENGTH = 500


def contains_exclude_patterns(text, exclude_patterns):
    for pattern in exclude_patterns:
        if re.compile(pattern).search(text):
            return True
    return False


def strip_patterns(text, remove_patterns):
    processed = text
    for pattern in remove_patterns:
        processed = re.sub(pattern, '', processed)
    return processed


# Use a new line for each sentence
def add_linebreaks(text):
    # Remove unnecessary linebreaks (remove because it leads to too many merged lines)
    # fixed_1 = re.sub(r'([^.?:;!])\n', r'\1 ', text)
    # Remove unnecessary whitespaces
    trimmed = re.sub(r'\n\s', r'\n', text)
    # Split sentences and avoid splitting on abbreviations or enumerations (e.g., e. V., 1., ...)
    return re.sub(r'([^\s.].[.?;!]"?)(\s|[A-Z][a-z])', r'\1\n\2', trimmed)


# Parse html and filter out paragraphs matching any of the exclude patterns
def parse_html(html, exclude_patterns):
    soup = BeautifulSoup(html, features='html.parser')

    for script in soup(['script', 'style', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        script.extract()

    for br in soup.find_all('br'):
        br.replace_with('\n')

    text = soup.get_text()

    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split('  '))
    text = add_linebreaks('\n'.join(chunk for chunk in chunks if chunk))
    lines = [re.sub(r' ', '', line).strip() for line in text.split('\n') if len(line) != 0 and not contains_exclude_patterns(line, exclude_patterns)]

    # parsed_paragraphs = []
    # # for paragraph in BeautifulSoup(html, 'html.parser').findAll('p'):
    # for paragraph in filter(tag_visible, BeautifulSoup(html, 'html.parser').findAll(text=True)):
    #     parsed_paragraph = paragraph
    #     if len(parsed_paragraph) != 0 and not contains_exclude_patterns(parsed_paragraph, exclude_patterns):
    #         parsed_paragraphs.append(re.sub(r' ', ' ', strip_patterns()))
    #
    # text = add_linebreaks('\n'.join(parsed_paragraphs))
    # lines = [line for line in text.split('\n') if len(line) != 0]

    return '\n'.join(lines)


# Fetch pages from cms.integreat-app.de
def load_data():
    os.makedirs(get_integreat_pages_path(''), exist_ok=True)
    response = requests.get(f'https://cms.integreat-app.de/api/{CITY}/{LANGUAGE}/pages').text
    f = open(get_integreat_pages_json_path(), 'w')
    f.write(response)


def preprocess():
    os.makedirs(get_integreat_pages_path(''), exist_ok=True)
    f = open(get_integreat_pages_json_path(), 'r')
    data = json.load(f)
    chars = 0

    page_dict = {}

    for page in data:
        # Remove duplicates (by titles)
        page_dict[page.get('title')] = [page.get('id'), page.get('content')]

    for title, value in page_dict.items():
        page_id = value[0]
        content = value[1]
        # if len(title) + len(content) < MIN_CONTENT_LENGTH:
        #     continue

        parsed = parse_html(content, [
            # Remove keyword list
            r'This text contains',
            r'Dieser Text enthält',
            r'Schlagworte:',
            # Remove phone numbers, addresses etc.
            r'[0-9]{4,}',
        ]).replace('  ', ' ')

        # if len(title) + len(parsed) < MIN_CONTENT_LENGTH:
        #     continue

        filename = get_integreat_pages_path(f'{page_id}.txt')
        new_file = open(filename, 'w')
        new_file.write(title + '\n' + parsed)

        chars += len(parsed)

    # Token ~= 0.75 word || token ~= 4 chars
    # No preprocessing: 102988 words
    # Preprocessing: 46585 words (289611 chars ~= 72400 input tokens ~= 72,4€)
    print(chars)


if __name__ == '__main__':
    # Uncomment to load data initially
    # load_data()
    preprocess()
    # postprocess()
