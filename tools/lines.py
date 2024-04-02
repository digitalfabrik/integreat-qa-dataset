import os
import os.path
import re
from constants import get_questions_with_evidence_path, RAW_SLUG, RESPONSES_SLUG


def extract(raw, key):
    line = next(line for line in raw if line.startswith(key))
    return line.split(f'{key}:')[1].strip()


def get_answer_lines(text):
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

    return lines


def postprocess():
    raw_dir_path = get_questions_with_evidence_path([RESPONSES_SLUG])
    slugs = os.listdir(raw_dir_path)
    print(slugs)

    for slug in slugs:
        raw_path = get_questions_with_evidence_path([RAW_SLUG, slug])
        raw_file = open(raw_path, 'r')
        raw_content = raw_file.readlines()

        try:
            for i in [1, 2, 3, 4, 5, 6, 7]:
                try:
                    answer = extract(raw_content, f'A{i}')
                    answer_lines = get_answer_lines(answer)
                    print(answer_lines, answer)
                except Exception:
                    continue
        except (StopIteration, ValueError):
            print(f'Failed to process {slug}')


if __name__ == '__main__':
    postprocess()
