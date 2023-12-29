import json
import os
import os.path
from constants import get_questions_with_evidence_path, get_integreat_pages_path, RAW_SLUG


def extract(raw, key):
    line = next(line for line in raw if line.startswith(key))
    return line.split(f'{key}:')[1].strip()


def postprocess():
    raw_dir_path = get_questions_with_evidence_path([RAW_SLUG])
    dataset_path = get_questions_with_evidence_path(['dataset.jsonl'])
    slugs = os.listdir(raw_dir_path)

    dataset = []

    for slug in slugs:
        raw_path = get_questions_with_evidence_path([RAW_SLUG, slug])
        page_path = get_integreat_pages_path(slug)

        raw_file = open(raw_path, 'r')
        raw_content = raw_file.readlines()

        page_file = open(page_path, 'r')
        page_content = page_file.read()

        try:
            questions = []
            for i in [1, 2, 3]:
                question = extract(raw_content, f'Q{i}')
                answer = extract(raw_content, f'A{i}')
                questions.append({'question': question, 'answer': answer})

            row = json.dumps({'context': page_content, 'questions': questions})
            dataset.append(row)
        except StopIteration:
            print(f'Failed to process {slug}')

    dataset_file = open(dataset_path, 'w')
    dataset_file.write('\n'.join(dataset))


if __name__ == '__main__':
    postprocess()
