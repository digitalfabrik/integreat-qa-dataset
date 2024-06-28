import json
import os
import os.path
import re

from transformers import pipeline, PretrainedConfig, AutoTokenizer
from torch import bfloat16

from constants import RAW_SLUG, LLAMA3_8B, LLAMA3_70B, LLAMA2_7B, PROMPT_v1, PROMPT_v2, IGEL, MIXTRAL8x7B, MIXTRAL8x22B, \
    MISTRAL, GPT, \
    RESPONSES_SLUG, PROMPT_v3, MISTRAL_MODELS, PROMPT_v4, MODELS, PROMPT_v5
from get_answer_prompt import get_answer_prompt
from evaluate_answers import evaluate

MODEL = MIXTRAL8x7B
MODEL_PATH = f'/hpc/gpfs2/scratch/g/coling/models/{MODEL}'

PROMPT_VERSION = PROMPT_v5
RUN = 0

DATASET_PATH = '../datasets/splits'


def extract_answer_lines(raw_input):
    try:
        answer_lines = []
        input = raw_input.replace('"', '')
        first_line = input.split('\n')[0]
        answers_start = input.index('[') + 1
        answers_end = input.index(']')

        matches_pattern = '[' in input and ']' in input
        # Extract text between brackets or first line otherwise
        raw_answers = first_line
        if matches_pattern:
            raw_answers = input[answers_start:answers_end]

        # Split answer parts
        answer_parts = [it.strip() for it in raw_answers.split(',')]

        for answer_part in answer_parts:
            if answer_part.isdigit():
                answer_lines.append(int(answer_part))
            elif re.match(r'[0-9]+\s*-\s*[0-9]+', answer_part):
                # Extend indices for ranges, e.g. '1-3' to '1,2,3'
                start, end = [it.strip() for it in answer_part.split('-')]
                if start.isdigit() and end.isdigit():
                    for index in range(int(start), int(end) + 1):
                        answer_lines.append(index)
        return answer_lines
    except Exception:
        return []


def postprocess_llm_answers(path):
    raw_dir_path = f'{path}/{RAW_SLUG}'
    predicted_path = f'{path}/predicted.json'
    slugs = os.listdir(raw_dir_path)

    predicted = {}
    matches_pattern = 0
    other_text = 0
    assistant = 0
    empty = 0

    for slug in slugs:
        raw_slug = slug.split('.txt')[0]
        raw_path = f'{raw_dir_path}/{slug}'
        raw_file = open(raw_path, 'r')
        raw_answer = raw_file.read()

        answer_lines = extract_answer_lines(raw_answer)
        predicted[raw_slug] = answer_lines
        if '[' in raw_answer and ']' in raw_answer:
            matches_pattern += 1
        if 'assistant' in raw_answer:
            assistant += 1
        if not raw_answer.startswith('[') or not raw_answer.endswith(']'):
            other_text += 1
        if len(answer_lines) == 0 and '[]' in raw_answer:
            empty += 1


    dataset_json_file = open(predicted_path, 'w')
    dataset_json_file.write(json.dumps(predicted))
    print(f'{matches_pattern}/{len(slugs)} ({round(matches_pattern/len(slugs), 2)}) | {assistant} | {other_text} | {empty} ({round(empty/len(slugs), 2)})')
    return predicted


# Add line numbers to each line
def enumerate_lines(text):
    lines = text.split('\n')
    numerated_lines = []
    for index, line in enumerate(lines):
        numerated_lines.append(f'[{str(index)}] {line}')
    return '\n'.join(numerated_lines)


def get_instruction(question, language):
    context = enumerate_lines(question['context'])
    prompt = get_answer_prompt(question['question'], context, PROMPT_VERSION, language)

    # mistralai models don't support the system role
    if MODEL in MISTRAL_MODELS:
        prompt = prompt[1:]

    return prompt


def instruction_generator(questions, language):
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    for question in questions:
        instruction = get_instruction(question, language)

        prompt = tokenizer.apply_chat_template(
            instruction,
            tokenize=False,
            add_generation_prompt=True
        )
        yield prompt


def get_all_answers(questions, path, language):
    counter = 0

    generate_text = pipeline(
        'text-generation',
        model=MODEL_PATH,
        config=PretrainedConfig(temperature=0.75),
        return_full_text=False,
        torch_dtype=bfloat16,
        device_map='auto',
        max_new_tokens=64
    )

    for response in generate_text(instruction_generator(questions, language)):
        question = questions[counter]
        question_id = question['id']
        raw_answer_path = f'{path}/{question_id}.txt'
        raw = response[0]['generated_text'].strip()

        raw_file = open(raw_answer_path, 'w')
        raw_file.write(raw)
        counter += 1


def get_all_answers_gpt(questions, path, language):
    for question in questions:
        question_id = question['id']
        # prompt_gpt(get_instruction(question, language), question_id, path)


if __name__ == '__main__':
    languages = ['fr']
    prompt_run = f'{PROMPT_VERSION}_{RUN}'

    for language in languages:
        CROSS_LANGUAGE = False
        question_language = 'de' if language == 'en' else 'en'
        language_slug = f'{language}_{question_language}' if CROSS_LANGUAGE else language
        base_answer_path = f'../answers/{MODEL}/{prompt_run}/{language_slug}'
        answer_path = f'{base_answer_path}/{RAW_SLUG}'
        os.makedirs(answer_path, exist_ok=True)

        dataset_path = f'{DATASET_PATH}/{language}/test_{language}.json'
        questions = json.load(open(dataset_path, 'r'))

        if CROSS_LANGUAGE:
            translated_dataset_path = f'{DATASET_PATH}/{question_language}/test_{question_language}.json'
            translated_dataset = json.load(open(translated_dataset_path, 'r'))
            questions = [{**question, 'question': next(translated['question'] for translated in translated_dataset if translated['id'] == question['id'])} for question in questions]

        if MODEL == GPT:
            os.makedirs(f'{base_answer_path}/{RESPONSES_SLUG}', exist_ok=True)
            get_all_answers_gpt(questions, base_answer_path, language)
        else:
            get_all_answers(questions, answer_path, language)

        predictions = postprocess_llm_answers(base_answer_path)
        evaluate(questions, predictions, MODEL, language)
