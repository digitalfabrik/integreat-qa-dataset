import json

import deepl
import os
from dotenv import load_dotenv

DATASET_PATH = f'../datasets/dataset.json'

load_dotenv()
DEEPL_API_KEY = os.getenv('DEEPL_API_KEY')
translator = deepl.Translator(DEEPL_API_KEY)


if __name__ == '__main__':
    questions_only = True
    source_language = 'uk'
    target_language = 'de'
    questions = json.load(open(f'../datasets/dataset_{source_language}.json')) # if questions_only else DATASET_PATH, 'r'))
    questions_source = [question for question in questions if question['language'] != target_language]
    questions_target = [question for question in questions if question['language'] == target_language]

    target_dataset_path = f'../datasets/dataset_{target_language}_retranslated_{source_language}.json' if questions_only else f'../datasets/dataset_{target_language}.json'
    raw_target_dataset = json.load(open(target_dataset_path, 'r')) if os.path.exists(target_dataset_path) else questions_target
    target_dataset = [question for question in raw_target_dataset if next((x for x in questions if x['id'] == question['id']), None) is not None]
    translated_questions = len(target_dataset) - len(questions_target)

    deepl_target = 'en-us' if target_language == 'en' else target_language
    new = questions_target
    base_target_dataset_path = f'../datasets/dataset_{target_language}.json'
    base_target_dataset = json.load(open(base_target_dataset_path, 'r')) if os.path.exists(base_target_dataset_path) else []

    print(translated_questions, len(questions_source))
    for question in questions_source:
        translated = next((x for x in target_dataset if x['id'] == question['id']), None)
        if translated is not None:
            new.append(translated)
        else:
            try:
                question_tr = translator.translate_text(question['question'], target_lang=deepl_target, source_lang=source_language).text
                print(question['question'], '|', question_tr)
                if questions_only:
                    base_translated = next((x for x in base_target_dataset if x['id'] == question['id']), None)
                    new.append({
                        **question,
                        'sourceLanguage': source_language,
                        'language': target_language,
                        'question': question_tr,
                        'context': base_translated['context']
                    })
                else:
                    context_lines_tr = []
                    context_lines = question['context'].split('\n')
                    for context_line in context_lines:
                        line_tr = translator.translate_text(context_line, target_lang=deepl_target, source_lang=source_language).text
                        context_lines_tr.append(line_tr)
                        print(context_line, '|', line_tr)
                    context_tr = '\n'.join(context_lines_tr)
                    new.append({
                        **question,
                        'sourceLanguage': source_language,
                        'language': target_language,
                        'question': question_tr,
                        'context': context_tr
                    })
            except Exception as e:
                print(e)
                break

    dataset_file = open(target_dataset_path, 'w')
    dataset_file.write(json.dumps(new))
    ids = set([question['id'] for question in target_dataset])
    print(len(ids))

    dataset_lines_file = open(f'{target_dataset_path}l', 'w')
    dataset_lines = [json.dumps(question) for question in new]
    dataset_lines_file.write('\n'.join(dataset_lines))
