import json
import os
import random
import csv

DATASET_PATH = f'../datasets/dataset.json'


def load_split(name, language):
    path = f'../datasets/splits/{language}/{name}_{language}.json'
    return json.load(open(path, 'r'))


if __name__ == '__main__':
    source_language = 'en'
    target_languages = ['ar', 'fr', 'uk']
    splits = ['train', 'dev', 'test']
    split_count = [2, 1, 1]
    sample_ids = [[1576, 3459], [4363], [3301]]

    for language in target_languages:
        os.makedirs(f'../translations', exist_ok=True)
        for index, split in enumerate(splits):
            source = load_split(split, source_language)
            target = load_split(split, language)
            ids = [x['id'] for x in source]
            for i in range(0, split_count[index]):
                # id = ids[random.randint(0, len(ids))] if language == target_languages[0] else sample_ids[index][i]
                id = sample_ids[index][i]
                if language == target_languages[0]:
                    sample_ids[index].append(id)

                translation_csv = open(f'../translations/{language}_{id}.csv', 'w')
                writer = csv.writer(translation_csv, delimiter=';', quotechar='"')
                writer.writerow([source_language, language, 'Fluency (Y/N)', 'Adequacy (Y/N)'])

                source_row = next((x for x in source if x['id'] == id), None)
                target_row = next((x for x in target if x['id'] == id), None)
                writer.writerow([source_row['question'], target_row['question']])
                source_sentences = source_row['context'].split('\n')
                target_sentences = target_row['context'].split('\n')
                for j, sentence in enumerate(source_sentences):
                    writer.writerow([sentence, target_sentences[j]])
