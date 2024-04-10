import json

import numpy as np
import pandas as pd

def print_w_percentage(value, reference):
    return f'({int(len(value) / len(reference) * 100)}%)'


if __name__ == '__main__':
    language = 'de'
    dataset = json.load(open(f'../datasets/dataset_{language}.json', 'r'))
    train = pd.DataFrame()
    dev = pd.DataFrame()
    test = pd.DataFrame()
    no_answer_source_language = []
    no_answer_translated = []
    one_answer_source_language = []
    one_answer_translated = []
    divided_answer_source_language = []
    divided_answer_translated = []
    other_answer_source_language = []
    other_answer_translated = []

    for row in dataset:
        answers = row['answers']
        if len(answers) == 0:
            if row['source_language'] is None:
                no_answer_source_language.append(row)
            else:
                no_answer_translated.append(row)
        elif len(answers) == 1:
            if row['source_language'] is None:
                one_answer_source_language.append(row)
            else:
                one_answer_translated.append(row)
        elif len(answers) > 0 and len(answers) != len(range(answers[0], answers[-1] + 1)):
            if row['source_language'] is None:
                divided_answer_source_language.append(row)
            else:
                divided_answer_translated.append(row)
        else:
            if row['source_language'] is None:
                other_answer_source_language.append(row)
            else:
                other_answer_translated.append(row)

    print(len(no_answer_source_language), len(no_answer_translated))
    print(len(one_answer_source_language), len(one_answer_translated))
    print(len(divided_answer_source_language), len(divided_answer_translated))
    print(len(other_answer_source_language), len(other_answer_translated))

    partitions = [no_answer_source_language, no_answer_translated, one_answer_source_language, one_answer_translated, divided_answer_source_language, divided_answer_translated, other_answer_source_language, other_answer_translated]

    for partition in partitions:
        _train, _dev, _test = np.split(pd.DataFrame(partition).sample(frac=1, random_state=420), [int(1 / 3 * len(partition) + 0.4), int(2 / 3 * len(partition) + 0.5)])
        train = pd.concat([train, _train])
        dev = pd.concat([dev, _dev])
        test = pd.concat([test, _test])

    print(len(train), len(dev), len(test))
    print(train.answers.str.len().mean(), dev.answers.str.len().mean(), test.answers.str.len().mean())
    print(train.context.str.len().mean(), dev.context.str.len().mean(), test.context.str.len().mean())


    def write_dataset(df, suffix='', language=language):
        df_file = open(f'../datasets/splits/{language}/{suffix}_{language}.json', 'w')
        df_file.write(df.to_json(orient='records'))
        df_file = open(f'../datasets/splits/{language}/{suffix}_{language}.jsonl', 'w')
        df_file.write(df.to_json(lines=True, orient='records'))
        return df

    write_dataset(train, 'train')
    write_dataset(dev, 'dev')
    write_dataset(test, 'test')

    other_languages = ['en']
    for language in other_languages:
        dataset = json.load(open(f'../datasets/dataset_{language}.json', 'r'))
        train = pd.DataFrame([next(x for x in dataset if x['id'] == row['id']) for _, row in train.iterrows()])
        dev = pd.DataFrame([next(x for x in dataset if x['id'] == row['id']) for _, row in dev.iterrows()])
        test = pd.DataFrame([next(x for x in dataset if x['id'] == row['id']) for _, row in test.iterrows()])

        write_dataset(train, 'train', language)
        write_dataset(dev, 'dev', language)
        write_dataset(test, 'test', language)


    for partition in [train, dev, test]:
        no_answer_source_language_num = []
        no_answer_translated_num = []
        one_answer_source_language_num = []
        one_answer_translated_num = []
        divided_answer_source_language_num = []
        divided_answer_translated_num = []
        other_answer_source_language_num = []
        other_answer_translated_num = []

        for _, row in partition.iterrows():
            answers = row['answers']
            if len(answers) == 0:
                if row['source_language'] is None:
                    no_answer_source_language_num.append(row)
                else:
                    no_answer_translated_num.append(row)
            elif len(answers) == 1:
                if row['source_language'] is None:
                    one_answer_source_language_num.append(row)
                else:
                    one_answer_translated_num.append(row)
            elif len(answers) > 0 and len(answers) != len(range(answers[0], answers[-1] + 1)):
                if row['source_language'] is None:
                    divided_answer_source_language_num.append(row)
                else:
                    divided_answer_translated_num.append(row)
            else:
                if row['source_language'] is None:
                    other_answer_source_language_num.append(row)
                else:
                    other_answer_translated_num.append(row)

        # print(len(no_answer_source_language_num) + len(no_answer_translated_num))
        # print(len(divided_answer_source_language_num) + len(divided_answer_translated_num))
        # print(len(other_answer_source_language_num) + len(other_answer_translated_num) + len(one_answer_source_language_num) + len(one_answer_translated_num))
        # print(len([x for _, x in partition.iterrows() if x['source_language'] is None]))
        # print(len([x for _, x in partition.iterrows() if x['source_language'] == 'de']))
        print(len(no_answer_source_language_num), len(no_answer_translated_num))
        print(len(divided_answer_source_language_num), len(divided_answer_translated_num))

        # print(no_answer_source_language_num, no_answer_source_language), print_w_percentage(no_answer_translated_num, no_answer_translated))
        # print(pd.DataFrame(no_answer_source_language_num).jaccard.mean(), pd.DataFrame(no_answer_translated_num).jaccard.mean())
        # print(print_w_percentage(one_answer_source_language_num, one_answer_source_language), print_w_percentage(one_answer_translated_num, one_answer_translated))
        # print(pd.DataFrame(one_answer_source_language_num).jaccard.mean(), pd.DataFrame(one_answer_translated_num).jaccard.mean())
        # print(print_w_percentage(divided_answer_source_language_num, divided_answer_source_language), print_w_percentage(divided_answer_translated_num, divided_answer_translated))
        # print(pd.DataFrame(divided_answer_source_language_num).jaccard.mean(), pd.DataFrame(divided_answer_translated_num).jaccard.mean())
        # print(print_w_percentage(other_answer_source_language_num, other_answer_source_language), print_w_percentage(other_answer_translated_num, other_answer_translated))
        # print(pd.DataFrame(other_answer_source_language_num).jaccard.mean(), pd.DataFrame(other_answer_translated_num).jaccard.mean())

