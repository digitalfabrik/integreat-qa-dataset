import ast
import json
import os
import os.path
from constants import get_questions_with_evidence_path, get_integreat_pages_path, RAW_SLUG, CITY, LANGUAGE, \
    get_integreat_pages_json_path, MODEL, RESPONSES_SLUG


def extract(raw, key):
    line = next(line for line in raw if line.startswith(key))
    return line.split(f'{key}:')[1].strip()


def postprocess():
    raw_dir_path = get_questions_with_evidence_path([RESPONSES_SLUG])
    dataset_json_lines_path = get_questions_with_evidence_path(['dataset.jsonl'])
    dataset_json_path = get_questions_with_evidence_path(['dataset.json'])
    slugs = os.listdir(raw_dir_path)

    f = open(get_integreat_pages_json_path(), 'r')
    raw_pages = json.load(f)

    dataset = []
    json_lines_dataset = []

    for slug in slugs:
        raw_path = get_questions_with_evidence_path([RAW_SLUG, slug])
        page_path = get_integreat_pages_path(slug)
        raw_content = []

        if os.path.isfile(raw_path):
            raw_file = open(raw_path, 'r')
            raw_content = raw_file.readlines()
        else:
            response_path = get_questions_with_evidence_path([RESPONSES_SLUG, slug])
            response_file = open(response_path, 'r')
            response_content = response_file.read()
            raw = ast.literal_eval(response_content)['choices'][0]['message']['content']
            raw_file = open(raw_path, 'w')
            raw_file.write(raw)
            raw_content = raw.split('\n')

        page_file = open(page_path, 'r')
        page_content = page_file.read()

        raw_page = next(x for x in raw_pages if x.get("id") == int(slug[:slug.index('.txt')]))
        page_path = raw_page.get("path")

        try:
            questions = []
            for i in [1, 2, 3, 4, 5, 6, 7]:
                try:
                    question = extract(raw_content, f'Q{i}')
                    answer = extract(raw_content, f'A{i}').split(", ")
                    answer_lines = [int(x) for x in answer]
                    questions.append({'question': question, 'answerLines': answer_lines})
                except Exception:
                    continue

            if len(questions) == 0:
                raise ValueError()

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
        except (StopIteration, ValueError):
            print(f'Failed to process {slug}')

    dataset_json_lines_file = open(dataset_json_lines_path, 'w')
    dataset_json_lines_file.write('\n'.join(json_lines_dataset))

    dataset_json_file = open(dataset_json_path, 'w')
    dataset_json_file.write(json.dumps(dataset))


if __name__ == '__main__':
    postprocess()
