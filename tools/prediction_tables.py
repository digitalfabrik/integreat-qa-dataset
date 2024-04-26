import json
import os.path

import pandas as pd

from constants import P_SELECTED_AGREEMENT, MODELS, PROMPTS, RUNS, PROMPT_v3, PROMPT_v4

answers_table = []
no_answers_table = []


def add_latex_table_row(values, table):
    indentation = ''
    table.append(f"{indentation} {' & '.join([f'{it}' for it in values])} \\\\")


def round_mean_std(means, stds, is_max):
    rounded_means = [f'{mean * 100:.1f}' for mean in means]
    rounded_stds = [f'\\textcolor{{gray}}{{\scriptsize $\pm$ {std * 100:.0f}}}' for std in stds] if stds is not None else [''] * len(means)
    return [f'\\textbf{{{rounded_means[index]}}}{rounded_stds[index]}' if is_max[index] else f'{rounded_means[index]}{rounded_stds[index]}' for index in range(len(means))]


def prepare_evaluation(questions, predictions):
    df = pd.DataFrame(questions)
    df['predicted'] = df.apply(lambda row: predictions[str(row.id)], axis=1)
    df['intersection'] = df.apply(lambda x: list(set(x.answers).intersection(set(x.predicted))), axis=1)
    df['union'] = df.apply(lambda x: list(set(x.answers).union(set(x.predicted))), axis=1)
    df['jaccard'] = df.apply(lambda x: len(x.intersection) / len(x.union) if len(x.union) > 0 else 1, axis=1)
    df['jaccard_cc'] = df.apply(lambda x: (x.jaccard - P_SELECTED_AGREEMENT) / (1 - P_SELECTED_AGREEMENT), axis=1)
    df['precision'] = df.apply(lambda x: len(x.intersection) / len(x.predicted) if len(x.predicted) > 0 else 1, axis=1)
    df['recall'] = df.apply(lambda x: len(x.intersection) / len(x.answers) if len(x.answers) > 0 else 1, axis=1)
    df['f1'] = df.apply(
        lambda x: 2 * (x.precision * x.recall) / (x.precision + x.recall) if x.precision + x.recall > 0 else 0, axis=1)
    return df


def evaluate(questions, predictions):
    all = pd.DataFrame(prepare_evaluation(questions, predictions))
    dataset_df = all[all.answers.str.len() > 0]
    columns = [dataset_df.precision, dataset_df.recall, dataset_df.f1, dataset_df.jaccard]
    return [column.mean() for column in columns], [column.std() for column in columns]


def evaluate_no_answer(questions, predictions):
    dataset_df = pd.DataFrame(prepare_evaluation(questions, predictions))
    true_positives = dataset_df[(dataset_df.answers.str.len() == 0) & (dataset_df.predicted.str.len() == 0)]
    retrieved = dataset_df[dataset_df.predicted.str.len() == 0]
    relevant = dataset_df[dataset_df.answers.str.len() == 0]
    precision = len(true_positives) / len(retrieved)
    recall = len(true_positives) / len(relevant)
    f1 = 2 * (precision * recall) / (precision + recall)
    return [precision, recall, f1]


if __name__ == '__main__':
    prompts = [PROMPT_v4, PROMPT_v3]
    languages = ['de', 'en']
    simple_metrics = ['precision', 'recall', 'f1']
    metrics = simple_metrics + ['jaccard']

    add_latex_table_row(['model', 'setting'] + len(languages) * metrics, answers_table)
    answers_table.append('\\midrule')
    add_latex_table_row(['model', 'setting'] + len(languages) * simple_metrics, no_answers_table)
    no_answers_table.append('\\midrule')

    labels = []
    means = []
    stds = []
    means_no_answer = []

    for model in MODELS:
        for prompt in prompts:
            model_name_parts = model.split('/')
            model_name = model_name_parts[-1].split('-Instruct')[0] if prompt == PROMPT_v4 else ''
            setting = '5-shot' if prompt == PROMPT_v3 else '0-shot'
            labels.append([model_name, setting])
            _means = []
            _stds = []
            _means_no_answer = []
            for language in ['de', 'en']:
                predictions_path = f'../answers/{model}/{prompt}_{0}/{language}/predicted.json'
                if os.path.exists(predictions_path):
                    predictions = json.load(open(predictions_path, 'r'))
                    dataset_path = f'../datasets/splits/{language}/dev_{language}.json'
                    questions = json.load(open(dataset_path, 'r'))
                    result = evaluate(questions, predictions)
                    _means += result[0]
                    _stds += result[1]
                    _means_no_answer += evaluate_no_answer(questions, predictions)
                elif language == 'de':
                    break
                else:
                    _means += [0, 0, 0, 0]
                    _stds += [0, 0, 0, 0]
                    _means_no_answer += [0, 0, 0]
            means.append(_means)
            stds.append(_stds)
            means_no_answer.append(_means_no_answer)

    mean_df = pd.DataFrame(means)
    for index in range(len(means)):
        add_latex_table_row(labels[index] + round_mean_std(means[index], stds[index], [maximum == index for maximum in mean_df.idxmax()]), answers_table)
        if index < len(means) - 1 and index % 2 == 1:
            answers_table.append('\\midrule')

    answers_table.append('\\bottomrule')
    table_file = open('./resources/answers.txt', 'w')
    table_file.write('\n'.join(answers_table))

    mean_no_answer_df = pd.DataFrame(means_no_answer)
    for index in range(len(means_no_answer)):
        add_latex_table_row(labels[index] + round_mean_std(means_no_answer[index], None, [maximum == index for maximum in mean_no_answer_df.idxmax()]), no_answers_table)
        if index < len(means_no_answer) - 1 and index % 2 == 1:
            no_answers_table.append('\\midrule')

    no_answers_table.append('\\bottomrule')
    table_file = open('./resources/no_answers.txt', 'w')
    table_file.write('\n'.join(no_answers_table))
