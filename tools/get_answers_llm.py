import json
import os
import os.path
import re

from transformers import pipeline, PretrainedConfig
from torch import bfloat16

from constants import RAW_SLUG, LLAMA3_8B, LLAMA3_70B, PROMPT_v1, PROMPT_v2, IGEL, MIXTRAL, MISTRAL, GPT, RESPONSES_SLUG
from get_answer_prompt import get_answer_prompt
from evaluate_answers import evaluate
from tools.prompt_gpt import prompt_gpt

MODEL = GPT
MODEL_PATH = f'/hpc/gpfs2/scratch/g/coling/models/{MODEL}'

PROMPT_VERSION = PROMPT_v2
RUN = 0

DATASET_PATH = '../datasets/splits'

def extract_answer(line):
    try:
        return line.split('Sentence numbers:')[1].split('\n')[0].strip()
    except Exception:
        return ''


def get_answer_lines(text):
    try:
        lines = []
        parts = [it.strip() for it in text.split(',')]

        for part in parts:
            if part.isdigit():
                lines.append(int(part))
            elif re.match(r'[0-9]+\s*-\s*[0-9]+', part):
                sub_parts = [it.strip() for it in part.split('-')]
                if sub_parts[0].isdigit() and sub_parts[1].isdigit():
                    for i in range(int(sub_parts[0]), int(sub_parts[1]) + 1):
                        lines.append(i)

        return lines
    except Exception:
        return


def postprocess_llm_answers(path):
    raw_dir_path = f'{path}/{RAW_SLUG}'
    predicted_path = f'{path}/predicted.json'
    slugs = os.listdir(raw_dir_path)

    predicted = {}

    for slug in slugs:
        raw_slug = slug.split('.txt')[0]
        raw_path = f'{raw_dir_path}/{slug}'
        raw_file = open(raw_path, 'r')
        raw_content = raw_file.read()

        raw_answer = extract_answer(raw_content)
        answer_lines = get_answer_lines(raw_answer)
        predicted[raw_slug] = answer_lines

    dataset_json_file = open(predicted_path, 'w')
    dataset_json_file.write(json.dumps(predicted))
    return predicted


def instruction_format(instructions):
    return f'<s> [INST] {instructions} [/INST]'


# Add line numbers to each line
def enumerate_lines(text):
    lines = text.split('\n')
    numerated_lines = []
    for index, line in enumerate(lines):
        numerated_lines.append(str(index) + ' ' + line)

    return '\n'.join(numerated_lines)


def get_instruction(question):
    context = enumerate_lines(question['context'])
    prompt = get_answer_prompt(question['question'], context, PROMPT_VERSION)
    instruction = instruction_format(prompt)
    # instruction = prompt
    return instruction


def instruction_generator(questions):
    for question in questions:
        instruction = get_instruction(question)
        yield instruction


def get_all_answers(questions, path):
    counter = 0

    generate_text = pipeline(
        'text-generation',
        model=MODEL_PATH,
        config=PretrainedConfig(temperature=0.75),
        return_full_text=False,
        torch_dtype=bfloat16,
        device_map='auto',
        max_new_tokens=512
    )

    for response in generate_text(instruction_generator(questions)):
        question = questions[counter]
        question_id = question['id']
        raw_answer_path = f'{path}/{question_id}.txt'
        raw = response[0]['generated_text'].strip()

        raw_file = open(raw_answer_path, 'w')
        raw_file.write(raw)
        counter += 1


def get_all_answers_gpt(questions, path):
    for question in questions:
        question_id = question['id']
        prompt_gpt(get_instruction(question), question_id, path)


if __name__ == '__main__':
    languages = ['de', 'en']
    prompt_run = f'{PROMPT_VERSION}_{RUN}'

    for language in languages:
        base_answer_path = f'../answers/{MODEL}/{prompt_run}/{language}'
        answer_path = f'{base_answer_path}/{RAW_SLUG}'
        os.makedirs(answer_path, exist_ok=True)
        dataset_path = f'{DATASET_PATH}/{language}/dev_{language}.json'
        questions = json.load(open(dataset_path, 'r'))

        if MODEL == GPT:
            os.makedirs(f'{base_answer_path}/{RESPONSES_SLUG}', exist_ok=True)
            get_all_answers_gpt(questions, base_answer_path)
        else:
            get_all_answers(questions, answer_path)

        predictions = postprocess_llm_answers(base_answer_path)
        evaluate(questions, predictions, MODEL, prompt_run, language)
