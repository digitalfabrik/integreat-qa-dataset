import json
import os.path

import pandas as pd

from constants import MODELS, PROMPTS, RUNS, PROMPT_v3, PROMPT_v4, LLAMA3_70B, get_model_name, \
    RAW_SLUG
from tools.get_answers_llm import extract_answer_lines
from tools.prediction_tables import add_latex_table_row

postprocessing_table = []


def print_with_percentages(absolutes, percentages):
    # rounded_percentages = [f'\\textcolor{{gray}}{{\scriptsize ({percentage * 100:.0f}\%)}}' for percentage in percentages]
    # return [f'{absolutes[index]}{rounded_percentages[index]}' for index in range(len(absolutes))]
    return [f'{percentage * 100:.1f}' for percentage in percentages]


def postprocess(path):
    raw_dir_path = f'{path}/{RAW_SLUG}'
    predicted_path = f'{path}/predicted.json'
    slugs = os.listdir(raw_dir_path)

    predicted = {}
    raw_answers = []

    for slug in slugs:
        raw_slug = slug.split('.txt')[0]
        raw_path = f'{raw_dir_path}/{slug}'
        raw_file = open(raw_path, 'r')
        raw_answer = raw_file.read()
        raw_answers.append(raw_answer)

        answer_lines = extract_answer_lines(raw_answer)
        predicted[raw_slug] = answer_lines


    dataset_json_file = open(predicted_path, 'w')
    dataset_json_file.write(json.dumps(predicted))
    return evaluate_postprocessing(raw_answers)


def evaluate_postprocessing(raw_answers):
    matches_pattern = 0
    other_text = 0
    assistant = 0
    unanswerable = 0
    invalid = 0

    x = 0

    for raw_answer in raw_answers:
        if '[' in raw_answer and ']' in raw_answer:
            matches_pattern += 1
        if not raw_answer.startswith('[') or not raw_answer.endswith(']'):
            other_text += 1
        if 'assistant' in raw_answer:
            assistant += 1
        if len(extract_answer_lines(raw_answer)) == 0:
            x += 1
            if '[]' in raw_answer:
                unanswerable += 1
            else:
                invalid += 1
    values = [matches_pattern, other_text, assistant, invalid, unanswerable]
    return values, [value / len(raw_answers) for value in values]


# TODO test partition only?
if __name__ == '__main__':
    prompts = [PROMPT_v4, PROMPT_v3]
    languages = ['de', 'en']
    columns = ['Pat.', 'Text', 'Assist.', 'Inv.', 'Unansw.']
    # columns = ['Pattern', 'Add. Text', 'Inv.', 'Unansw.']

    add_latex_table_row(['Model', 'Setting'] + 2 * columns, postprocessing_table)
    postprocessing_table.append('\\midrule')

    labels = []
    absolutes = []
    percentages = []

    for model in MODELS:
        for prompt in prompts:
            setting = '5-shot' if prompt == PROMPT_v3 else '0-shot'
            model_name = get_model_name(model) if prompt == PROMPT_v4 else ''
            labels.append([model_name, setting])
            _absolutes = []
            _percentages = []

            for language in ['de', 'en']:
                answers_path = f'../answers/{model}/{prompt}_{0}/{language}'
                result = postprocess(answers_path)
                _absolutes += result[0]
                _percentages += result[1]
            absolutes.append(_absolutes)
            percentages.append(_percentages)

    absolutes_df = pd.DataFrame(absolutes[:-2])
    for index in range(len(absolutes)):
        add_latex_table_row(labels[index] + print_with_percentages(absolutes[index], percentages[index]), postprocessing_table)
        if index % 2 == 1 and index != len(absolutes) - 1:
            postprocessing_table.append('\\midrule')

    postprocessing_table.append('\\bottomrule')
    table_file = open('./resources/postprocessing.txt', 'w')
    table_file.write('\n'.join(postprocessing_table))
