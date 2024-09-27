import json

import numpy as np
import pandas as pd

SPLITS = [0.5, 0.72]


def print_w_percentage(value, reference):
    return f'({int(len(value) / len(reference) * 100)}%)'


def separated_filter(row):
    return len(row.answers) > 0 and len(row.answers) != len(range(row.answers[0], row.answers[-1] + 1))

def other_filter(row):
    return len(row.answers) > 0 and len(row.answers) == len(range(row.answers[0], row.answers[-1] + 1))


if __name__ == '__main__':
    language = 'de'
    dataset_df = pd.DataFrame(json.load(open(f'../datasets/dataset_{language}.json', 'r')))
    # dataset_df['question_word'] = dataset_df.apply(lambda x: x.question.split(' ')[0], axis=1)
    # print('Question words')
    # print('\n'.join([f'{key}: {value}' for key, value in dataset_df.question_word.value_counts()[dataset_df.question_word.value_counts() > 5].items()]))
    # print(f'Other {dataset_df.question_word.value_counts()[dataset_df.question_word.value_counts() <= 5].sum()}')
    train = pd.DataFrame()
    dev = pd.DataFrame()
    test = pd.DataFrame()

    source_df = dataset_df[dataset_df.sourceLanguage.isnull()]
    translated_df = dataset_df[dataset_df.sourceLanguage == 'en']

    for partition0 in [source_df, translated_df]:
        munich_df = partition0[partition0.city == 'muenchen']
        augsburg_df = partition0[partition0.city == 'lkaugsburg']
        rems_df = partition0[partition0.city == 'rems-murr-kreis']

        for partition1 in [munich_df, augsburg_df, rems_df]:
            single_questions_df = partition1[partition1.duplicated(keep=False, subset=['pageId']) == False]
            no_answers_df = single_questions_df[single_questions_df.answers.str.len() == 0]
            divided_answers_df = single_questions_df[single_questions_df.apply(separated_filter, axis=1)]
            other_answers_df = single_questions_df[single_questions_df.apply(other_filter, axis=1)]
            random_state = 22

            for partition2 in [no_answers_df, divided_answers_df, other_answers_df]:
                _train, _dev, _test = np.split(pd.DataFrame(partition2).sample(frac=1, random_state=random_state), [int(SPLITS[0] * len(partition2)), int(SPLITS[1] * len(partition2))])
                train = pd.concat([train, _train])
                dev = pd.concat([dev, _dev])
                test = pd.concat([test, _test])

            multiple_questions_df = partition1[partition1.duplicated(keep=False, subset=['pageId'])]
            multiple_page_ids = multiple_questions_df.pageId.sample(frac=1, random_state=random_state).unique()
            for index, page_id in enumerate(multiple_page_ids):
                rows = multiple_questions_df[multiple_questions_df.pageId == page_id]
                if index / len(multiple_page_ids) < SPLITS[0]:
                    train = pd.concat([train, rows])
                elif index / len(multiple_page_ids) < SPLITS[1]:
                        dev = pd.concat([dev, rows])
                else:
                    test = pd.concat([test, rows])

    print(len(train), len(dev), len(test))
    print(train.answers.str.len().mean(), dev.answers.str.len().mean(), test.answers.str.len().mean())
    print(train.context.str.len().mean(), dev.context.str.len().mean(), test.context.str.len().mean())
    print(len(train[train.answers.str.len() == 0]), len(dev[dev.answers.str.len() == 0]), len(test[test.answers.str.len() == 0]))
    print(len(train[train.apply(separated_filter, axis=1)]), len(dev[dev.apply(separated_filter, axis=1)]), len(test[test.apply(separated_filter, axis=1)]))


    def write_dataset(df, suffix='', language=language):
        df_file = open(f'../datasets/splits/{language}/{suffix}_{language}.json', 'w')
        df_file.write(df.to_json(orient='records'))
        df_file = open(f'../datasets/splits/{language}/{suffix}_{language}.jsonl', 'w')
        df_file.write(df.to_json(lines=True, orient='records'))
        return df

    write_dataset(train, 'train')
    write_dataset(dev, 'dev')
    write_dataset(test, 'test')

    other_languages = ['en', 'fr', 'ar', 'uk', 'de_retranslated_ar', 'de_retranslated_fr', 'de_retranslated_uk']
    for language in other_languages:
        dataset = json.load(open(f'../datasets/dataset_{language}.json', 'r'))
        train = pd.DataFrame([next(x for x in dataset if x['id'] == row['id']) for _, row in train.iterrows()])
        dev = pd.DataFrame([next(x for x in dataset if x['id'] == row['id']) for _, row in dev.iterrows()])
        test = pd.DataFrame([next(x for x in dataset if x['id'] == row['id']) for _, row in test.iterrows()])

        write_dataset(train, 'train', language)
        write_dataset(dev, 'dev', language)
        write_dataset(test, 'test', language)



    # for partition in [train, dev, test]:
    #     no_answer_sourceLanguage_num = []
    #     no_answer_translated_num = []
    #     one_answer_sourceLanguage_num = []
    #     one_answer_translated_num = []
    #     divided_answer_sourceLanguage_num = []
    #     divided_answer_translated_num = []
    #     other_answer_sourceLanguage_num = []
    #     other_answer_translated_num = []
    #
    #     for _, row in partition.iterrows():
    #         answers = row['answers']
    #         if len(answers) == 0:
    #             if row['sourceLanguage'] is None:
    #                 no_answer_sourceLanguage_num.append(row)
    #             else:
    #                 no_answer_translated_num.append(row)
    #         elif len(answers) == 1:
    #             if row['sourceLanguage'] is None:
    #                 one_answer_sourceLanguage_num.append(row)
    #             else:
    #                 one_answer_translated_num.append(row)
    #         elif len(answers) > 0 and len(answers) != len(range(answers[0], answers[-1] + 1)):
    #             if row['sourceLanguage'] is None:
    #                 divided_answer_sourceLanguage_num.append(row)
    #             else:
    #                 divided_answer_translated_num.append(row)
    #         else:
    #             if row['sourceLanguage'] is None:
    #                 other_answer_sourceLanguage_num.append(row)
    #             else:
    #                 other_answer_translated_num.append(row)
    #
    #     print(len(no_answer_sourceLanguage_num) + len(no_answer_translated_num))
    #     print(len(divided_answer_sourceLanguage_num) + len(divided_answer_translated_num))
    #     print(len(other_answer_sourceLanguage_num) + len(other_answer_translated_num) + len(one_answer_sourceLanguage_num) + len(one_answer_translated_num))
    #     print(len([x for _, x in partition.iterrows() if x['sourceLanguage'] is None]))
    #     print(len([x for _, x in partition.iterrows() if x['sourceLanguage'] == 'de']))
    #     print(len(no_answer_sourceLanguage_num), len(no_answer_translated_num))
    #     print(len(divided_answer_sourceLanguage_num), len(divided_answer_translated_num))
    #
    #     print(no_answer_sourceLanguage_num, no_answer_sourceLanguage), print_w_percentage(no_answer_translated_num, no_answer_translated))
    #     print(pd.DataFrame(no_answer_sourceLanguage_num).jaccard.mean(), pd.DataFrame(no_answer_translated_num).jaccard.mean())
    #     print(print_w_percentage(one_answer_sourceLanguage_num, one_answer_sourceLanguage), print_w_percentage(one_answer_translated_num, one_answer_translated))
    #     print(pd.DataFrame(one_answer_sourceLanguage_num).jaccard.mean(), pd.DataFrame(one_answer_translated_num).jaccard.mean())
    #     print(print_w_percentage(divided_answer_sourceLanguage_num, divided_answer_sourceLanguage), print_w_percentage(divided_answer_translated_num, divided_answer_translated))
    #     print(pd.DataFrame(divided_answer_sourceLanguage_num).jaccard.mean(), pd.DataFrame(divided_answer_translated_num).jaccard.mean())
    #     print(print_w_percentage(other_answer_sourceLanguage_num, other_answer_sourceLanguage), print_w_percentage(other_answer_translated_num, other_answer_translated))
    #     print(pd.DataFrame(other_answer_sourceLanguage_num).jaccard.mean(), pd.DataFrame(other_answer_translated_num).jaccard.mean())