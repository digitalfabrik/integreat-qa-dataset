import json
import os.path

import pandas as pd

from constants import P_SELECTED_AGREEMENT, MODELS, PROMPTS, RUNS, PROMPT_v3, PROMPT_v4, LLAMA3_70B
from evaluate_answers import prepare_evaluation
from tools.prediction_tables import add_latex_table_row, evaluate, evaluate_no_answer, round_mean_std

answers_table = []


if __name__ == '__main__':

    prompts = [PROMPT_v4]
    metrics = ['P', 'R', 'F']

    add_latex_table_row(['Document', 'Question'] + 2 * metrics, answers_table)
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
                    full_document_language = 'German' if document_language == 'de' else 'English'
                    full_question_language = 'German' if question_language == 'de' else 'English'
                    labels.append([full_document_language, full_question_language])

                    predictions_path = f'../answers/{model}/{prompt}_{0}/{language}/predicted.json'
                    predictions = json.load(open(predictions_path, 'r'))
                    dataset_path = f'../datasets/splits/{document_language}/test_{document_language}.json'
                    questions = json.load(open(dataset_path, 'r'))

                    _means += evaluate(questions, predictions)[0]
                    _means += evaluate_no_answer(questions, predictions)
                    means.append(_means)

    mean_df = pd.DataFrame(means)
    for index in range(len(means)):
        add_latex_table_row(labels[index] + round_mean_std(means[index], None, [False for maximum in mean_df.idxmax()]), answers_table)
        if index < len(means) - 1 and index % 2 == 1:
            answers_table.append('\\midrule')

    answers_table.append('\\bottomrule')
    table_file = open('./resources/cross_language_answers.txt', 'w')
    table_file.write('\n'.join(answers_table))
