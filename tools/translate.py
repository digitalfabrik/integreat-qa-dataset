import json

import deepl
import os
from dotenv import load_dotenv

DATASET_PATH = f'../datasets/dataset.json'

load_dotenv()
DEEPL_API_KEY = os.getenv('DEEPL_API_KEY')
translator = deepl.Translator(DEEPL_API_KEY)


if __name__ == '__main__':
    source_language = 'en'
    target_language = 'de'
    questions = json.load(open(DATASET_PATH, 'r'))
    questions_source = [question for question in questions if question['language'] == source_language]
    questions_target = [question for question in questions if question['language'] == target_language]

    target_dataset_path = f'../datasets/dataset_{target_language}.json'
    ready_questions = len(json.load(open(target_dataset_path, 'r'))) - len(questions_target) if os.path.exists(target_dataset_path) else 0

    deepl_target = 'en-us' if target_language == 'en' else target_language

    print(ready_questions, len(questions_source))
    for question in questions_source[ready_questions:]:
        try:
            question_tr = translator.translate_text(question['question'], target_lang=deepl_target, source_lang=source_language).text
            print(question['question'], '|', question_tr)
            context_lines_tr = []
            context_lines = question['context'].split('\n')
            for context_line in context_lines:
                line_tr = translator.translate_text(context_line, target_lang=deepl_target, source_lang=source_language).text
                context_lines_tr.append(line_tr)
                print(context_line, '|', line_tr)
            context_tr = '\n'.join(context_lines_tr)
            questions_target.append({
                **question,
                'source_language': source_language,
                'language': target_language,
                'question': question_tr,
                'context': context_tr
            })
        except Exception as e:
            print(e)
            break

    dataset_file = open(target_dataset_path, 'w')
    dataset_file.write(json.dumps(questions_target))

    dataset_lines_file = open(f'${target_dataset_path}l', 'w')
    dataset_lines = [json.dumps(question) for question in questions_target]
    dataset_lines_file.write('\n'.join(dataset_lines))

# print(f'English: {en}, German: {len(questions) - en},  Total: {len(questions)}')
