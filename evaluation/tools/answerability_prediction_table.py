import json
import os.path

import pandas as pd

from constants import P_SELECTED_AGREEMENT, MODELS, PROMPTS, RUNS, PROMPT_v3, PROMPT_v4, LLAMA3_70B, LLAMA3_8B, \
    MIXTRAL8x7B, get_model_name, DEBERTA, MISTRAL, GPT, PROMPT_v5
from evaluate_answers import prepare_evaluation
from tools.get_answers_llm import evaluate_unanswerability
from tools.prediction_tables import add_latex_table_row, evaluate, evaluate_no_answer, round_mean_std

answers_table = []


if __name__ == '__main__':
    prompts = [PROMPT_v4, PROMPT_v3]
    languages = ['de', 'en']
    simple_metrics = ['P', 'R', 'F']
    metrics = simple_metrics
    # metrics = simple_metrics + ['jaccard']

    add_latex_table_row(['Model', 'Setting'] + 2 * metrics + [''] + 2 * metrics, answers_table)
    answers_table.append('\\cmidrule{1 - 8}\\cmidrule{10 - 15}')

    labels = []
    means = []
    means_no_answer = []

    for model in [LLAMA3_70B, DEBERTA]:
        for prompt in prompts:
            if model == DEBERTA and prompt == prompts[1]:
                continue
            setting = '5-shot' if prompt == PROMPT_v3 else '0-shot'
            model_name = get_model_name(model) if prompt == PROMPT_v4 else ''
            labels.append([model_name, '$-$' if model == DEBERTA else setting])
            _means = []
            _means_no_answer = []
            paths = []
            paths.append(f'../train/{model}/unanswerable/de/standard/predicted.json' if model == DEBERTA else f'../answers/{model}/{PROMPT_v5}_{0}/de/predicted.json')
            paths.append(f'../train/{model}/unanswerable/en/standard/predicted.json' if model == DEBERTA else f'../answers/{model}/{PROMPT_v5}_{0}/en/predicted.json')
            paths.append(f'../train/{model}/answers/de/context_3_standard/predicted.json' if model == DEBERTA else f'../answers/{model}/{prompt}_{0}/de/predicted.json')
            paths.append(f'../train/{model}/answers/en/context_3_standard/predicted.json' if model == DEBERTA else f'../answers/{model}/{prompt}_{0}/en/predicted.json')
            for path in paths:
                if path == paths[2]:
                    _means += ['']
                if os.path.exists(path) and not ((path == paths[0] or path == paths[1]) and prompt == PROMPT_v3):
                    predictions = json.load(open(path, 'r'))
                    dataset_path = f'../datasets/splits/de/test_de.json'
                    questions = json.load(open(dataset_path, 'r'))
                    result = evaluate_no_answer(questions, predictions) if path == paths[2] or path == paths[3] else evaluate_unanswerability(questions, predictions)
                    _means += result
                else:
                    _means += ['$-$', '$-$', '$-$']
            print(model)
            means.append(_means)
    print(means)

    mean_df = pd.DataFrame(means[:-2])
    for index in range(len(means)):
        add_latex_table_row(
            labels[index] + round_mean_std(means[index], None, None),
            answers_table)
        if index % 2 == 1:
            answers_table.append('\\cmidrule{1 - 8}\\cmidrule{10 - 15}')

    answers_table.append('\\bottomrule')
    table_file = open('./resources/explicit_answerability.txt', 'w')
    table_file.write('\n'.join(answers_table))
