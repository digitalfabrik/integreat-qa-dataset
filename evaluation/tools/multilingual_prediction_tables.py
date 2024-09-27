import json
import os.path

import pandas as pd

from constants import P_SELECTED_AGREEMENT, MODELS, PROMPTS, RUNS, PROMPT_v3, PROMPT_v4, LLAMA3_70B, LLAMA3_8B, \
    MIXTRAL8x7B, get_model_name, DEBERTA, MISTRAL, GPT
from evaluate_answers import prepare_evaluation
from tools.prediction_tables import add_latex_table_row, evaluate, evaluate_no_answer, round_mean_std

answers_table = []


if __name__ == '__main__':
    prompts = [PROMPT_v4]
    languages = ['de', 'en', 'ar', 'fr', 'uk']
    simple_metrics = ['P', 'R', 'F']
    metrics = simple_metrics
    # metrics = simple_metrics + ['jaccard']

    add_latex_table_row(['Model', 'Lang.'] + 2 * metrics + [''] + 2 * metrics, answers_table)
    # answers_table.append('\\midrule')
    answers_table.append('\\cmidrule{1 - 8}\\cmidrule{10 - 15}')

    labels = []
    means = []
    stds = []
    means_no_answer = []

    # for model in MODELS:
    for model in [MIXTRAL8x7B, LLAMA3_8B, LLAMA3_70B, DEBERTA]:
    #     for prompt in prompts:
        for prompt in [PROMPT_v4]:
            for language in languages:
                model_name = get_model_name(model) if language == 'de' else ''
                labels.append([model_name, language])
                _means = []
                _stds = []
                _means_no_answer = []
                for translation in ['', 'de_retranslated_']:
                    predictions_path = f'../train/{model}/answers/{translation}{language}/context_3_standard/predicted.json' if model == DEBERTA else f'../answers/{model}/{prompt}_{0}/{translation}{language}/predicted.json'
                    if os.path.exists(predictions_path):
                        predictions = json.load(open(predictions_path, 'r'))
                        dataset_path = f'../datasets/splits/{language}/test_{language}.json'
                        questions = json.load(open(dataset_path, 'r'))
                        result = evaluate(questions, predictions)
                        _means += result[0]
                        _stds += result[1]
                        _means_no_answer += evaluate_no_answer(questions, predictions)
                    else:
                        _means += ['$-$', '$-$', '$-$']
                        _stds += [0, 0, 0]
                        _means_no_answer += ['$-$', '$-$', '$-$']
                means.append(_means + [''] + _means_no_answer)
                stds.append(_stds)
                means_no_answer.append(_means_no_answer)

    dataset_path = f'../datasets/splits/de/test_de.json'
    questions = json.load(open(dataset_path, 'r'))
    # means.append((['$-$', '$-$', result[0][2]] * 2) + [''] + (['$-$', '$-$', '$-$'] * 2))

    mean_df = pd.DataFrame(means)
    for index in range(len(means)):
        add_latex_table_row(labels[index] + round_mean_std(means[index], None, None), answers_table)
        if index % 5 == 4 and index != len(means) - 1:
            answers_table.append('\\cmidrule{1 - 8}\\cmidrule{10 - 15}')

    answers_table.append('\\bottomrule')
    # answers_table.append('\\cmidrule{1 - 8}\\cmidrule{10 - 15}')
    table_file = open('./resources/multilingual_answers.txt', 'w')
    table_file.write('\n'.join(answers_table))
