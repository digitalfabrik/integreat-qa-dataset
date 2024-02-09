import json
import os
import os.path
from constants import get_questions_with_evidence_path, get_integreat_pages_path, CITY, LANGUAGE, \
    get_integreat_pages_json_path, MODEL, READY_SLUG, get_dataset_path


def extract(raw, key):
    line = next(line for line in raw if line.startswith(key))
    return line.split(f'{key}:')[1].strip()


def postprocess():
    ready_dir_path = get_questions_with_evidence_path([READY_SLUG])
    dataset_json_lines_path = get_dataset_path('jsonl')
    dataset_json_path = get_dataset_path('json')
    slugs = os.listdir(ready_dir_path)

    f = open(get_integreat_pages_json_path(), 'r')
    raw_pages = json.load(f)

    dataset = []
    json_lines_dataset = []

    for slug in slugs:
        ready_path = get_questions_with_evidence_path([READY_SLUG, slug])
        page_path = get_integreat_pages_path(slug)

        ready_file = open(ready_path, 'r')
        ready_content = ready_file.read()
        if not ready_content:
            continue
        questions = json.loads(ready_content)

        page_file = open(page_path, 'r')
        page_content = page_file.read()

        raw_page = next(x for x in raw_pages if x.get("id") == int(slug[:slug.index('.txt')]))
        page_path = raw_page.get("path")

        if len(questions) == 0:
            continue

        row = {
            'pageId': slug[:slug.index('.txt')],
            'questions': questions,
            'pagePath': page_path,
            'city': CITY,
            'language': LANGUAGE,
            'model': MODEL,
            'context': page_content
        }
        dataset.append(row)
        json_lines_dataset.append(json.dumps(row))

    dataset_json_lines_file = open(dataset_json_lines_path, 'w')
    dataset_json_lines_file.write('\n'.join(json_lines_dataset))

    dataset_json_file = open(dataset_json_path, 'w')
    dataset_json_file.write(json.dumps(dataset))


if __name__ == '__main__':
    postprocess()
