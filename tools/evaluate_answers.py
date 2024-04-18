import json
import os
import os.path
import re
from constants import RAW_SLUG, get_answers_path

DATASET_PATH = f'../datasets/2024-04-01_dataset.json'


def extract_answer(line):
    try:
        return line.split('## Numbers:')[1].split('##')[0].strip()
    except Exception:
        print(line)
        return ''


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


def postprocess_llm_answers(path, questions):
    raw_dir_path = f'{path}/{RAW_SLUG}'
    predicted_path = f'{path}/predicted.json'
    slugs = os.listdir(raw_dir_path)

    predicted = {}

    correct_answer = 0
    answer_count = 0
    correct_no_answer = 0
    no_answer = 0
    no_answer_2 = 0

    for slug in slugs:
        raw_slug = slug.split('.txt')[0]
        raw_path = f'{raw_dir_path}/{slug}'
        raw_file = open(raw_path, 'r')
        raw_content = raw_file.readline()

        question = next(x for x in questions if x['id'] == int(raw_slug))

        raw_answer = extract_answer(raw_content)
        answer_lines = get_answer_lines(raw_answer)
        predicted[raw_slug] = answer_lines

        lines = question['context'].split('\n')
        answer = '\n'.join([f'[{line}] {lines[line]}' for line in answer_lines if line < len(lines)])

        if len(question['answers']) != 0:
            if len(answer) == 0:
                no_answer_2 += 1
            answer_count += 1
            # print(question['question'])
            # print(answer)
            # print('\n')
            # predicted_line_number = question['context'][:prediction['start']].count('\n')
            # predicted_in_annotated = predicted_line_number in question['answers']
            # if predicted_in_annotated:
            #     correct_answer += 1
        else:
            print(question['question'])
            print(answer if len(answer) > 0 else '---')
            if len(answer) == 0:
                no_answer_2 += 1
            print('\n')
            no_answer += 1
            if len(answer_lines) == 0:
                correct_no_answer += 1

    # print(correct_answer, answer_count, correct_answer / answer_count)
    # print(correct_no_answer, no_answer, correct_no_answer / no_answer)
    # print((correct_answer + correct_no_answer) / len(questions))
    print(no_answer_2, no_answer)
    print(len(questions) - no_answer_2)
    print(len(questions))
    print(predicted)

    dataset_json_file = open(predicted_path, 'w')
    dataset_json_file.write(json.dumps(predicted))


if __name__ == '__main__':
    postprocess_llm_answers('', [])
