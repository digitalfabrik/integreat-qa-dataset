import json
import os
import os.path
from constants import get_questions_with_evidence_path, get_integreat_pages_path, RAW_SLUG, \
    RESPONSES_SLUG, READY_SLUG


def extract(raw, key):
    line = next(line.strip() for line in raw if line.strip().startswith(key))
    return line.split(f'{key}:')[1].strip()


def confirm_question(slug, title, question, answer_lines):
    text = input(f'{slug} | {title} | {question}')
    new_question = ''
    if len(text) == 0:
        new_question = question
    elif text == 'd':
        return None
    elif text == 'a':
        new_question = question.split('?')[0] + title + '?'
    else:
        new_question = text

    return {'question': new_question, 'answerLines': answer_lines}


def add_context():
    raw_dir_path = get_questions_with_evidence_path([RAW_SLUG])
    slugs = os.listdir(raw_dir_path)

    for slug in slugs:
        ready_path = get_questions_with_evidence_path([READY_SLUG, slug])

        if os.path.isfile(ready_path):
            continue

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
                answer = extract(raw_content, f'A{i}')
                try:
                    answer_lines = [int(x.strip()) for x in answer.split(",")]
                except Exception:
                    answer_lines = [-1]

                confirmed_question = confirm_question(slug, page_content.split('\n')[0], question, answer_lines)
                if confirmed_question is not None:
                    questions.append(confirmed_question)
            except Exception as e:
                if i < 4:
                    print(e)
                continue

        ready_file = open(ready_path, 'w')
        ready_file.write(json.dumps(questions))


if __name__ == '__main__':
    os.makedirs(get_questions_with_evidence_path([READY_SLUG]), exist_ok=True)
    add_context()
