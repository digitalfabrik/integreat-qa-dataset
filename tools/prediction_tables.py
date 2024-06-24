import json
import os.path

import pandas as pd

from constants import P_SELECTED_AGREEMENT, ALL_MODELS, PROMPTS, RUNS, PROMPT_v3, PROMPT_v4, LLAMA3_70B, get_model_name, DEBERTA
from evaluate_answers import prepare_evaluation

answers_table = []
no_answers_table = []


def add_latex_table_row(values, table):
    indentation = ''
    table.append(f"{indentation} {' & '.join([f'{it}' for it in values])} \\\\")


def round_mean_std(means, stds, is_max):
    rounded_means = [f'{mean * 100:.1f}' if not isinstance(mean, str) else mean for mean in means]
    rounded_stds = [f'\\textcolor{{gray}}{{\scriptsize $\pm$ {std * 100:.0f}}}' for std in stds] if stds is not None else [''] * len(means)
    return [f'\\textbf{{{rounded_means[index]}}}{rounded_stds[index]}' if is_max[index] else f'{rounded_means[index]}{rounded_stds[index]}' for index in range(len(means))]


def f1(a, b):
    return 2 * (a * b) / (a + b)


def evaluate(questions, predictions):
    all = pd.DataFrame(prepare_evaluation(questions, predictions))
    dataset_df = all[all.answers.str.len() > 0]
    columns = [dataset_df.precision, dataset_df.recall]
    means = [column.mean() for column in columns]
    return means + [f1(means[0], means[1])], [column.std() for column in columns]


def evaluate_no_answer(questions, predictions):
    dataset_df = pd.DataFrame(prepare_evaluation(questions, predictions))
    true_positives = dataset_df[(dataset_df.answers.str.len() == 0) & (dataset_df.predicted.str.len() == 0)]
    retrieved = dataset_df[dataset_df.predicted.str.len() == 0]
    relevant = dataset_df[dataset_df.answers.str.len() == 0]
    print(len(set(retrieved.id).intersection(set(relevant.id))), len(retrieved), len(relevant))
    precision = len(true_positives) / len(retrieved)
    recall = len(true_positives) / len(relevant)
    return [precision, recall, f1(precision, recall)]


if __name__ == '__main__':
    prompts = [PROMPT_v4, PROMPT_v3]
    languages = ['de', 'en']
    simple_metrics = ['P', 'R', 'F']
    metrics = simple_metrics
    # metrics = simple_metrics + ['jaccard']

    add_latex_table_row(['Model', 'Setting'] + 2 * metrics + [''] + 2 * metrics, answers_table)
    # answers_table.append('\\midrule')
    answers_table.append('\\cmidrule{1 - 8}\\cmidrule{10 - 15}')
    add_latex_table_row(['Model', 'Setting'] + 4 * simple_metrics, no_answers_table)
    no_answers_table.append('\\midrule')

    labels = []
    means = []
    stds = []
    means_no_answer = []

    for model in ALL_MODELS:
    # for model in [LLAMA3_70B]:
        for prompt in prompts:
            if model == DEBERTA and prompt == prompts[1]:
                continue
            setting = '5-shot' if prompt == PROMPT_v3 else '0-shot'
            model_name = get_model_name(model) if prompt == PROMPT_v4 else ''
            labels.append([model_name, '$-$' if model == DEBERTA else setting])
            _means = []
            _stds = []
            _means_no_answer = []
            for language in ['de', 'en']:
                predictions_path = f'../train/{model}/answers/{language}/context_3_standard/predicted.json' if model == DEBERTA else f'../answers/{model}/{prompt}_{0}/{language}/predicted.json'
                if os.path.exists(predictions_path):
                    predictions = json.load(open(predictions_path, 'r'))
                    dataset_path = f'../datasets/splits/{language}/test_{language}.json'
                    questions = json.load(open(dataset_path, 'r'))
                    result = evaluate(questions, predictions)
                    _means += result[0]
                    _stds += result[1]
                    _means_no_answer += evaluate_no_answer(questions, predictions)
                elif language == 'de':
                    break
                else:
                    _means += [0, 0, 0]
                    _stds += [0, 0, 0]
                    _means_no_answer += [0, 0, 0]
            means.append(_means + [''] + _means_no_answer)
            stds.append(_stds)
            means_no_answer.append(_means_no_answer)

    human_annotator0_path = f'../answers/human/wo_adjacent/annotator0/predicted.json'
    human_annotator1_path = f'../answers/human/wo_adjacent/annotator1/predicted.json'
    human_annotations0 = json.load(open(human_annotator0_path, 'r'))
    human_annotations1 = json.load(open(human_annotator1_path, 'r'))
    dataset_path = f'../datasets/splits/de/test_de.json'
    questions = json.load(open(dataset_path, 'r'))
    questions = [{**question, 'answers': human_annotations1[str(question['id'])]} for question in questions]

    result = evaluate(questions, human_annotations0)
    means.append((['-', '-', result[0][2]] * 2) + [''] + (['-', '-', '-'] * 2))

    human_annotator0_path = f'../answers/human/w_adjacent/annotator0/predicted.json'
    human_annotator1_path = f'../answers/human/w_adjacent/annotator1/predicted.json'
    human_annotations0 = json.load(open(human_annotator0_path, 'r'))
    human_annotations1 = json.load(open(human_annotator1_path, 'r'))
    dataset_path = f'../datasets/splits/de/test_de.json'
    questions = json.load(open(dataset_path, 'r'))
    questions = [{**question, 'answers': human_annotations1[str(question['id'])]} for question in questions]

    result = evaluate(questions, human_annotations0)
    means.append((['$-$', '$-$', result[0][2]] * 2) + [''] + (['$-$', '$-$', '$-$'] * 2))
    print(means)

    mean_df = pd.DataFrame(means[:-2])
    for index in range(len(means)):
        if index < len(means) - 2:
            add_latex_table_row(labels[index] + round_mean_std(means[index], None, [maximum == index for maximum in mean_df.idxmax()]), answers_table)
            if index % 2 == 1:
                answers_table.append('\\cmidrule{1 - 8}\\cmidrule{10 - 15}')
        elif index == len(means) - 2:
            answers_table.append('\cmidrule[\heavyrulewidth]{1 - 8}\cmidrule[\heavyrulewidth]{10 - 15}')
            add_latex_table_row(['Human Upper Bound', ''] + round_mean_std(means[index], None, [maximum == index for maximum in mean_df.idxmax()]), answers_table)
        elif index == len(means) - 1:
            add_latex_table_row(['Human Upper Bound', ''] + round_mean_std(means[index], None, [maximum == index for maximum in mean_df.idxmax()]), answers_table)

    # answers_table.append('\\bottomrule')
    answers_table.append('\\cmidrule{1 - 8}\\cmidrule{10 - 15}')
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
