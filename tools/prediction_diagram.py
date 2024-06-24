import pandas as pd
from matplotlib import pyplot as plt
import json
from evaluate_answers import prepare_evaluation
from constants import MODELS, PROMPTS, RUNS, LLAMA3_70B, PROMPT_v4, GPT, MIXTRAL8x7B
from tools.prediction_tables import f1

plt.rcParams.update({'font.size': 23})

plt, axis = plt.subplots(figsize=(11, 7))
axis.set_title('')


if __name__ == '__main__':
    languages = ['en']

    # for model in [LLAMA3_70B]:
    #     for language in languages:
    #         predictions_path = f'../answers/{LLAMA3_70B}/v4_0/{language}/predicted.json'
    #         dataset_path = f'../datasets/splits/{language}/dev_{language}.json'
    #         predictions = json.load(open(predictions_path, 'r'))
    #         questions = json.load(open(dataset_path, 'r'))
    #         evaluation_df = prepare_evaluation(questions, predictions)
    #         grouped_df = evaluation_df[evaluation_df.answer_count < 19].groupby(evaluation_df.answer_count)
    #         precisions = grouped_df.precision.mean().plot.line(ax=axis, marker='s', label='precision', markersize=17,
    #                                                            linewidth=3)
    #         recalls = grouped_df.recall.mean().plot.line(ax=axis, marker='^', label='recall', markersize=17,
    #                                                      linewidth=3)
    # axis.set_xlabel('ground truth answers')
    # axis.set_xticks([1, 2, 4, 6, 8, 10, 12, 14, 16])
    # axis.legend()
    # plt.savefig('resources/precision_recall_answers.pdf', format='pdf')

    for language in languages:
        precisions = []
        recalls = []
        f1s = []
        for setting in ['context_0_standard', 'context_1_standard', 'context_2_standard', 'context_3_standard', 'context_4_standard', 'context_5_standard']:
            predictions_path = f'../train/deberta-v3-large/answers/{language}/{setting}/predicted_dev.json'
            dataset_path = f'../datasets/splits/{language}/dev_{language}.json'
            predictions = json.load(open(predictions_path, 'r'))
            questions = json.load(open(dataset_path, 'r'))
            evaluation_df = prepare_evaluation(questions, predictions)
            precision = evaluation_df.precision.mean()
            precisions.append(precision)
            recall = evaluation_df.recall.mean()
            recalls.append(recall)
            f1s.append(f1(precision, recall))
        pd.DataFrame(precisions).plot.line(ax=axis, marker='s', label='P', markersize=17, linewidth=3)
        pd.DataFrame(recalls).plot.line(ax=axis, marker='^', label='R', markersize=17, linewidth=3)
        pd.DataFrame(f1s).plot.line(ax=axis, marker='o', label='F', markersize=17, linewidth=3)
    axis.set_xlabel('adjacent context sentences')
    axis.set_xticks([0, 1, 2, 3, 4, 5])
    axis.set_ylim([0.55, 0.8])
    axis.legend(['P', 'R', 'F'])
    plt.savefig('resources/context_finetuning.pdf', format='pdf', bbox_inches='tight')
