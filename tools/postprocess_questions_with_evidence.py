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

    for slug_with_extension in slugs:
        slug = slug_with_extension[:slug_with_extension.index('.txt')]
        raw_path = get_questions_with_evidence_path([RAW_SLUG, slug_with_extension])
        page_path = get_integreat_pages_path(slug_with_extension)

        raw_file = open(raw_path, 'r')
        raw_content = raw_file.readlines()

        page_file = open(page_path, 'r')
        page_content = page_file.read()

        questions = []
        for i in [1, 2, 3]:
            question = extract(raw_content, f'Q{i}')
            answer = extract(raw_content, f'A{i}')
            questions.append({'question': question, 'answer': answer})

        row = json.dumps({'context': page_content, 'questions': questions})
        dataset.append(row)

    dataset_file = open(dataset_path, 'w')
    dataset_file.write('\n'.join(dataset))


if __name__ == '__main__':
    postprocess()
