import json
import os.path

import pandas as pd

from constants import P_SELECTED_AGREEMENT, MODELS, PROMPTS, RUNS, PROMPT_v3, PROMPT_v4, LLAMA3_70B
from evaluate_answers import prepare_evaluation

answers_table = []
no_answers_table = []


def add_latex_table_row(values, table):
    indentation = ''
    table.append(f"{indentation} {' & '.join([f'{it}' for it in values])} \\\\")


def round_mean_std(means, stds, is_max):
    rounded_means = [f'{mean * 100:.1f}' for mean in means]
    rounded_stds = [f'\\textcolor{{gray}}{{\scriptsize $\pm$ {std * 100:.0f}}}' for std in stds] if stds is not None else [''] * len(means)
    return [f'\\textbf{{{rounded_means[index]}}}{rounded_stds[index]}' if is_max[index] else f'{rounded_means[index]}{rounded_stds[index]}' for index in range(len(means))]


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

    prompts = [PROMPT_v4]
    metrics = ['P.', 'R.']

    add_latex_table_row(['Doc.', 'Q.'] + 2 * metrics, answers_table)
    answers_table.append('\\midrule')

    labels = []
    means = []
    languages = ['de', 'en']

    for model in [LLAMA3_70B]:
        for prompt in prompts:
            for document_language in languages:
                for question_language in languages if document_language == 'de' else reversed(languages):
                    _means = []
                    language = document_language if document_language == question_language else f'{document_language}_{question_language}'
                    full_document_language = 'Ger.' if document_language == 'de' else 'Eng.'
                    full_question_language = 'Ger.' if question_language == 'de' else 'Eng.'
                    labels.append([full_document_language, full_question_language])

                    predictions_path = f'../answers/{model}/{prompt}_{0}/{language}/predicted.json'
                    predictions = json.load(open(predictions_path, 'r'))
                    dataset_path = f'../datasets/splits/{document_language}/dev_{document_language}.json'
                    questions = json.load(open(dataset_path, 'r'))

                    _means += evaluate(questions, predictions)[0][:2]
                    _means += evaluate_no_answer(questions, predictions)[:2]
                    means.append(_means)

    mean_df = pd.DataFrame(means)
    for index in range(len(means)):
        add_latex_table_row(labels[index] + round_mean_std(means[index], None, [False for maximum in mean_df.idxmax()]), answers_table)
        if index < len(means) - 1 and index % 2 == 1:
            answers_table.append('\\midrule')

    answers_table.append('\\bottomrule')
    table_file = open('./resources/cross_language_answers.txt', 'w')
    table_file.write('\n'.join(answers_table))
