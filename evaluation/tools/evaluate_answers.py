import json
import os.path

import pandas as pd

from constants import P_SELECTED_AGREEMENT, MODELS, PROMPTS, RUNS, PROMPT_v3, PROMPT_v4, LLAMA3_70B, ORIGINAL

FIRST_COLUMN_WIDTH = 45
COLUMN_WIDTH = 15


def print_row(values):
    print(f'{values[0]:^{FIRST_COLUMN_WIDTH}} |', ' | '.join([f'{it:^{COLUMN_WIDTH}}' for it in values[1:]]))


def print_row_rounded(values):
    print_row(values[:2] + [f'{it.mean():.2f} ({it.std():.2f})' if isinstance(it, pd.Series) else f'{it:.2f}' for it in values[2:]])


def prepare_evaluation(questions, predictions):
    df = pd.DataFrame(questions)
    df['answer_count'] = df.apply(lambda row: len(row.answers), axis=1)
    df['predicted'] = df.apply(lambda row: predictions[str(row.id)], axis=1)
    df['intersection'] = df.apply(lambda x: list(set(x.answers).intersection(set(x.predicted))), axis=1)
    df['union'] = df.apply(lambda x: list(set(x.answers).union(set(x.predicted))), axis=1)
    df['jaccard'] = df.apply(lambda x: len(x.intersection) / len(x.union) if len(x.union) > 0 else 1, axis=1)
    df['jaccard_cc'] = df.apply(lambda x: (x.jaccard - P_SELECTED_AGREEMENT) / (1 - P_SELECTED_AGREEMENT), axis=1)
    df['precision'] = df.apply(lambda x: len(x.intersection) / len(x.predicted) if len(x.predicted) > 0 else 1, axis=1)
    df['recall'] = df.apply(lambda x: len(x.intersection) / len(x.answers) if len(x.answers) > 0 else 1, axis=1)
    df['f1'] = df.apply(lambda x: 2 * (x.precision * x.recall) / (x.precision + x.recall) if x.precision + x.recall > 0 else 0, axis=1)
    return df


def evaluate(questions, predictions, model, language):
    model_name_parts = model.split('/')
    model_name = model_name_parts[-1] if language == 'de' else ''
    all = pd.DataFrame(prepare_evaluation(questions, predictions))
    dataset_df = all[all.answers.str.len() > 0]
    print_row_rounded([model_name, language, dataset_df.precision, dataset_df.recall, dataset_df.f1, dataset_df.jaccard, dataset_df[dataset_df.predicted.str.len() > 0].predicted.str.len(), len(all[all.predicted.str.len() == 0]) / len(all)])


def evaluate_no_answer(questions, predictions, model, language):
    dataset_df = pd.DataFrame(prepare_evaluation(questions, predictions))
    true_positives = dataset_df[(dataset_df.answers.str.len() == 0) & (dataset_df.predicted.str.len() == 0)]
    retrieved = dataset_df[dataset_df.predicted.str.len() == 0]
    relevant = dataset_df[dataset_df.answers.str.len() == 0]
    precision = len(true_positives) / len(retrieved)
    recall = len(true_positives) / len(relevant)
    f1 = 2 * (precision * recall) / (precision + recall)
    print_row_rounded([model, language, precision, recall, f1])


if __name__ == '__main__':
    prompts = [PROMPT_v4, PROMPT_v3]
    columns = ['model', 'language', 'precision', 'recall', 'f1', 'jaccard', 'predictions', 'invalid/no answer']
    print_row(columns)
    row_length = FIRST_COLUMN_WIDTH + (len(columns) - 1) * (COLUMN_WIDTH + 3)
    print('-' * row_length)

    for model in MODELS:
        if model == ORIGINAL:
            predictions_path = f'../answers/{model}/predicted.json'
            if os.path.exists(predictions_path):
                predictions = json.load(open(predictions_path, 'r'))
                dataset_path = f'../datasets/dataset.json'
                questions = json.load(open(dataset_path, 'r'))
                questions = [question for question in questions if question['id'] in predictions.keys()]
                evaluate(questions, predictions, model, '-')
        else:
            for prompt in prompts:
                for run in RUNS:
                    prompt_run = f'{prompt}_{run}'
                    for language in ['de', 'en']:
                        predictions_path = f'../answers/{model}/{prompt_run}/{language}/predicted.json'
                        if os.path.exists(predictions_path):
                            predictions = json.load(open(predictions_path, 'r'))
                            dataset_path = f'../datasets/splits/{language}/dev_{language}.json'
                            questions = json.load(open(dataset_path, 'r'))
                            evaluate(questions, predictions, model, language)
        print('-' * row_length)


    print('')
    print('')
    columns = ['model', 'language', 'precision', 'recall', 'f1']
    print_row(columns)
    row_length = FIRST_COLUMN_WIDTH + (len(columns) - 1) * (COLUMN_WIDTH + 3)
    print('-' * row_length)

    for model in MODELS:
        for prompt in PROMPTS:
            for run in RUNS:
                prompt_run = f'{prompt}_{run}'
                for language in ['de', 'en']:
                    predictions_path = f'../answers/{model}/{prompt_run}/{language}/predicted.json'
                    if os.path.exists(predictions_path):
                        predictions = json.load(open(predictions_path, 'r'))
                        dataset_path = f'../datasets/splits/{language}/dev_{language}.json'
                        questions = json.load(open(dataset_path, 'r'))
                        evaluate_no_answer(questions, predictions, model, language)
        print('-' * row_length)
