import json
import os.path


def extract(raw, key):
    line = next(line.strip() for line in raw if line.strip().startswith(key))
    return line.split(f'{key}:')[1].strip()


if __name__ == '__main__':
    dataset = json.load(open(f'../datasets/dataset.json', 'r'))

    for row in dataset:
        language = row['language']
        city = row['city']
        pageId = row['pageId']
        question = row['question']

        w_evidence_path = f'../data/questions_with_evidence_Mixtral-8x7B-Instruct-v0.1/{city}/{language}/raw/{pageId}.txt'
        wo_evidence_path = f'../data/questions_wo_evidence_Mixtral-8x7B-Instruct-v0.1/{city}/{language}/raw/{pageId}.txt'

        raw_content_w_evidence = open(w_evidence_path, 'r').readlines() if os.path.exists(w_evidence_path) else []
        raw_content_wo_evidence = open(wo_evidence_path, 'r').readlines() if os.path.exists(wo_evidence_path) else []

        questions = []
        for i in [1, 2, 3, 4, 5, 6, 7]:
            try:
                questions.append(extract(raw_content_w_evidence, f'Q{i}'))
            except:
                continue

        for i in [1, 2, 3, 4, 5, 6, 7]:
            try:
                questions.append(extract(raw_content_wo_evidence, f'Q{i}'))
            except:
                continue

        if question not in questions:
            print(question, questions)
