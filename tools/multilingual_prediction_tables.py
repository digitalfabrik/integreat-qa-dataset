import json
import os.path

import pandas as pd

from constants import P_SELECTED_AGREEMENT, MODELS, PROMPTS, RUNS, PROMPT_v3, PROMPT_v4, LLAMA3_70B, LLAMA3_8B, MIXTRAL8x7B, get_model_name
from evaluate_answers import prepare_evaluation

answers_table = []


def add_latex_table_row(values, table):
    indentation = ''
    table.append(f"{indentation} {' & '.join([f'{it}' for it in values])} \\\\")


def round_mean_std(means, stds, is_max):
    rounded_means = [f'{mean * 100:.1f}' if not isinstance(mean, str) else mean for mean in means]
    rounded_stds = [f'\\textcolor{{gray}}{{\scriptsize $\pm$ {std * 100:.0f}}}' for std in stds] if stds is not None else [''] * len(means)
    return [f'{rounded_means[index]}{rounded_stds[index]}' for index in range(len(means))]


def evaluate(questions, predictions):
    all = pd.DataFrame(prepare_evaluation(questions, predictions))
    dataset_df = all[all.answers.str.len() > 0]
    # columns = [dataset_df.precision, dataset_df.recall, dataset_df.f1, dataset_df.jaccard]
    columns = [dataset_df.precision, dataset_df.recall, dataset_df.f1]
    # print(dataset_df.f1.mean(), dataset_df.jaccard.mean())
    return [column.mean() for column in columns], [column.std() for column in columns]


def evaluate_no_answer(questions, predictions):
    dataset_df = pd.DataFrame(prepare_evaluation(questions, predictions))
    true_positives = dataset_df[(dataset_df.answers.str.len() == 0) & (dataset_df.predicted.str.len() == 0)]
    retrieved = dataset_df[dataset_df.predicted.str.len() == 0]
    relevant = dataset_df[dataset_df.answers.str.len() == 0]
    print(len(set(retrieved.id).intersection(set(relevant.id))), len(retrieved), len(relevant))
    precision = len(true_positives) / len(retrieved)
    recall = len(true_positives) / len(relevant)
    f1 = 2 * (precision * recall) / (precision + recall)
    return [precision, recall, f1]


if __name__ == '__main__':
    prompts = [PROMPT_v4]
    languages = ['de', 'en', 'ar', 'fr', 'uk']
    simple_metrics = ['P', 'R', 'F']
    metrics = simple_metrics
    # metrics = simple_metrics + ['jaccard']

    add_latex_table_row(['Model', 'Language'] + 2 * metrics + [''] + 2 * metrics, answers_table)
    # answers_table.append('\\midrule')
    answers_table.append('\\cmidrule{1 - 8}\\cmidrule{10 - 15}')

    labels = []
    means = []
    stds = []
    means_no_answer = []

    # for model in MODELS:
    for model in [LLAMA3_70B, LLAMA3_8B]:
    #     for prompt in prompts:
        for prompt in [PROMPT_v4]:
            for language in languages:
                model_name = get_model_name(model)
                labels.append([model_name, language])
                _means = []
                _stds = []
                _means_no_answer = []
                for translation in ['', 'de_retranslated_']:
                    predictions_path = f'../answers/{model}/{prompt}_{0}/{translation}{language}/predicted.json'
                    if os.path.exists(predictions_path):
                        predictions = json.load(open(predictions_path, 'r'))
                        dataset_path = f'../datasets/splits/{language}/dev_{language}.json'
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

    dataset_path = f'../datasets/splits/de/dev_de.json'
    questions = json.load(open(dataset_path, 'r'))
    # means.append((['$-$', '$-$', result[0][2]] * 2) + [''] + (['$-$', '$-$', '$-$'] * 2))

    mean_df = pd.DataFrame(means[:-2])
    for index in range(len(means)):
        add_latex_table_row(labels[index] + round_mean_std(means[index], None, []), answers_table)
        if index % 5 == 4 and index != len(means) - 1:
            answers_table.append('\\cmidrule{1 - 8}\\cmidrule{10 - 15}')

    answers_table.append('\\bottomrule')
    # answers_table.append('\\cmidrule{1 - 8}\\cmidrule{10 - 15}')
    table_file = open('./resources/answers.txt', 'w')
    table_file.write('\n'.join(answers_table))
