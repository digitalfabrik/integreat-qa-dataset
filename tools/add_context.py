import json
import os
import os.path
from constants import get_questions_with_evidence_path, get_integreat_pages_path, RAW_SLUG, \
    RESPONSES_SLUG, READY_SLUG


def extract(raw, key):
    line = next(line for line in raw if line.startswith(key))
    return line.split(f'{key}:')[1].strip()


def confirm_question(slug, title, question, answer_lines):
    os.system('clear')
    text = input(f'{slug} | {title} | {question}')
    new_question = ''
    if len(text) == 0:
        new_question = question
    elif text == 'a':
        new_question = question.split('?')[0] + title + '?'
    else:
        new_question = text

    if question != new_question:
        return {'question': new_question, 'answerLines': answer_lines, 'previous': question}
    return {'question': new_question, 'answerLines': answer_lines}


def add_context():
    raw_dir_path = get_questions_with_evidence_path([RESPONSES_SLUG])
    slugs = os.listdir(raw_dir_path)

    for slug in slugs:
        ready_path = get_questions_with_evidence_path([READY_SLUG, slug])

        if os.path.isfile(ready_path):
            continue

        ready_file = open(ready_path, 'w')
        raw_path = get_questions_with_evidence_path([RAW_SLUG, slug])
        page_path = get_integreat_pages_path(slug)
        raw_file = open(raw_path, 'r')
        raw_content = raw_file.readlines()

        page_file = open(page_path, 'r')
        page_content = page_file.read()

        questions = []
        for i in [1, 2, 3, 4, 5, 6, 7]:
            try:
                question = extract(raw_content, f'Q{i}')
                answer = extract(raw_content, f'A{i}').split(", ")
                answer_lines = [int(x) for x in answer]
                questions.append(confirm_question(slug, page_content.split('\n')[0], question, answer_lines))
            except Exception:
                continue

        if len(questions) > 0:
            ready_file.write(json.dumps(questions))


if __name__ == '__main__':
    add_context()
