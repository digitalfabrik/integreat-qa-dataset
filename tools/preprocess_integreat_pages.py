import os
import requests
import json
import re
from bs4 import BeautifulSoup
from constants import get_integreat_pages_path, get_integreat_pages_json_path, CITY, LANGUAGE


MIN_CONTENT_LENGTH = 500


def contains_exclude_patterns(text, exclude_patterns):
    for pattern in exclude_patterns:
        if re.compile(pattern).search(text):
            return True
    return False


# Use a new line for each sentence
def add_linebreaks(text):
    # Remove unnecessary linebreaks (remove because it leads to too many merged lines)
    # fixed_1 = re.sub(r'([^.?:;!])\n', r'\1 ', text)
    # Remove unnecessary whitespaces
    trimmed = re.sub(r'\n\s', r'\n', text)
    # Split sentences and avoid splitting on abbreviations or enumerations (e.g., e. V., 1., ...)
    return re.sub(r'([^\s.].[.?:;!])\s', r'\1\n', trimmed)


# Parse html and filter out paragraphs matching any of the exclude patterns
def parse_html(html, exclude_patterns):
    parsed_paragraphs = []
    for paragraph in BeautifulSoup(html, 'html.parser').findAll('p'):
        parsed_paragraph = paragraph.text
        if not contains_exclude_patterns(parsed_paragraph, exclude_patterns):
            parsed_paragraphs.append(parsed_paragraph)

    text = add_linebreaks('\n'.join(parsed_paragraphs))
    lines = [line for line in text.split('\n') if len(line) != 0]

    return '\n'.join(lines)


# Fetch pages from cms.integreat-app.de
def load_data():
    os.makedirs(get_integreat_pages_path(''), exist_ok=True)
    response = requests.get(f'https://cms.integreat-app.de/api/{CITY}/{LANGUAGE}/pages').text
    f = open(get_integreat_pages_json_path(), 'w')
    f.write(response)


def preprocess():
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
        if len(title) + len(content) < MIN_CONTENT_LENGTH:
            continue

        parsed = parse_html(content, [
            # Remove keyword list
            r'This text contains information about the following search terms',
            r'This text contains information on the following search terms',
            r'Dieser Text enthält Informationen zu folgenden Suchbegriffen',
            # Remove phone numbers, addresses etc.
            r'[0-9]{4,}',
            # Remove non-breaking spaces
            r' '
        ]).replace('  ', ' ')

        if len(title) + len(parsed) < MIN_CONTENT_LENGTH:
            continue

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
