import json
import os.path
import re


def extract(raw, key):
    line = next(line.strip() for line in raw if line.strip().startswith(key))
    return line.split(f'{key}:')[1].strip()


def get_answer_lines(text):
    try:
        lines = []
        parts = [it.strip() for it in text.split(',')]

        for part in parts:
            if part.isdigit():
                lines.append(int(part))
            elif re.match(r'[0-9]+\s*-\s*[0-9]+', part):
                sub_parts = [it.strip() for it in part.split('-')]
                if sub_parts[0].isdigit() and sub_parts[1].isdigit():
                    for i in range(int(sub_parts[0]), int(sub_parts[1]) + 1):
                        lines.append(i)

        if -1 in lines or len(lines) == 0:
            print(text)
        return lines
    except Exception:
        print(text)
        return


if __name__ == '__main__':
    dataset = json.load(open(f'../datasets/dataset.json', 'r'))
    original_answer_lines = {}

    for row in dataset:
        language = row['language']
        city = row['city']
        pageId = row['pageId']
        question = row['question']
        id = row['id']

        w_evidence_path = f'../data/questions_with_evidence_Mixtral-8x7B-Instruct-v0.1/{city}/{language}/raw/{pageId}.txt'

        raw_content_w_evidence = open(w_evidence_path, 'r').readlines() if os.path.exists(w_evidence_path) else []

        answer_lines = None
        for i in [1, 2, 3, 4, 5, 6, 7]:
            try:
                if question == extract(raw_content_w_evidence, f'Q{i}'):
                    raw_answer_lines = extract(raw_content_w_evidence, f'A{i}')
                    answer_lines = get_answer_lines(raw_answer_lines)
                    original_answer_lines = {
                        **original_answer_lines,
                        id: answer_lines
                    }
            except:
                continue

    original_answer_lines_file = open(f'../answers/original/predicted.json', 'w')
    original_answer_lines_file.write(json.dumps(original_answer_lines))
