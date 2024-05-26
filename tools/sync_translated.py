import json

DATASET_PATH = f'../datasets/dataset.json'

if __name__ == '__main__':
    language = 'en'
    source_questions = json.load(open(DATASET_PATH, 'r'))
    target_path = f'../datasets/dataset_{language}.json'
    target_questions = json.load(open(target_path, 'r'))

    new_questions = []

    for target in target_questions:
        source = next((x for x in source_questions if x['id'] == target['id']), None)
        if source is not None:
            new_questions.append({
                **source,
                'sourceLanguage': target['sourceLanguage'],
                'language': target['language'],
                'context': target['context'],
                'question': target['question']
            })

    dataset_file = open(target_path, 'w')
    dataset_file.write(json.dumps(new_questions))

    dataset_lines_file = open(f'{target_path}l', 'w')
    dataset_lines = [json.dumps(question) for question in new_questions]
    dataset_lines_file.write('\n'.join(dataset_lines))
