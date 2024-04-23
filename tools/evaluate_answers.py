import json
import os.path

import pandas as pd

from constants import P_SELECTED_AGREEMENT, MODELS, PROMPTS, RUNS


def print_row(values, width=15):
    print(f'{values[0]:^45} |', ' | '.join([f'{it:^{width}}' for it in values[1:]]))


def print_row_rounded(values, width=15):
    print_row(values[:2] + [f'{it:.2f}' for it in values[2:]], width=width)


def prepare_evaluation(questions, predictions):
    df = pd.DataFrame(questions)
    df['predicted'] = df.apply(lambda row: predictions[str(row.id)], axis=1)
    df['intersection'] = df.apply(lambda x: list(set(x.answers).intersection(set(x.predicted))), axis=1)
    df['union'] = df.apply(lambda x: list(set(x.answers).union(set(x.predicted))), axis=1)
    df['jaccard'] = df.apply(lambda x: len(x.intersection) / len(x.union) if len(x.union) > 0 else 1, axis=1)
    df['jaccard_cc'] = df.apply(lambda x: (x.jaccard - P_SELECTED_AGREEMENT) / (1 - P_SELECTED_AGREEMENT), axis=1)
    df['precision'] = df.apply(lambda x: len(x.intersection) / len(x.predicted) if len(x.predicted) > 0 else 1, axis=1)
    df['recall'] = df.apply(lambda x: len(x.intersection) / len(x.answers) if len(x.answers) > 0 else 1, axis=1)
    df['f1'] = df.apply(lambda x: 2 * (x.precision * x.recall) / (x.precision + x.recall) if x.precision + x.recall > 0 else 0, axis=1)
    return df


def evaluate(questions, predictions, model, prompt, language):
    dataset_df = pd.DataFrame(prepare_evaluation(questions, predictions))
    print_row_rounded([f'{model} ({prompt})', language, dataset_df.precision.mean(), dataset_df.recall.mean(), dataset_df.f1.mean(), dataset_df.jaccard.mean(), dataset_df[dataset_df.predicted.str.len() > 0].predicted.str.len().mean(), len(dataset_df[dataset_df.predicted.str.len() == 0]) / len(dataset_df)])


if __name__ == '__main__':
    row_length = 175
    print_row(['model', 'language', 'precision', 'recall', 'f1', 'jaccard', 'predictions', 'no answer'])
    print('-' * 175)

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
                        evaluate(questions, predictions, model, prompt_run, language)
        print('-' * 175)
