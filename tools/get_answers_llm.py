import json
import os
import os.path
from transformers import pipeline
from torch import bfloat16

from constants import RAW_SLUG
from evaluate_answers import postprocess_llm_answers
from get_answer_prompt import get_answer_prompt

MIXTRAL = 'mistralai/Mixtral-8x7B-Instruct-v0.1'
MISTRAL = 'mistralai/Mistral-7B-Instruct-v0.2'
LLAMA2 = 'meta-llama/Llama-2-7b-hf'

PROMPT_VERSION = 'v1'
MODEL = LLAMA2
MODEL_PATH = f'/hpc/gpfs2/scratch/g/coling/models/{MODEL}'
DATASET_PATH = '../datasets/splits'

generate_text = pipeline(
    'text-generation',
    model=MODEL_PATH,
    return_full_text=False,
    torch_dtype=bfloat16,
    device_map='auto',
    max_new_tokens=512
)


def instruction_format(instructions):
    # return f'<s> [INST] {instructions} [/INST]\nUser: {query}\nAssistant: '
    return f'<s> [INST] {instructions} [/INST]'


# Add line numbers to each line
def enumerate_lines(text):
    lines = text.split('\n')
    numerated_lines = []
    for index, line in enumerate(lines):
        numerated_lines.append(str(index) + ' ' + line)

    return '\n'.join(numerated_lines)


def instruction_generator(questions):
    for question in questions:
        context = enumerate_lines(question['context'])
        # instruction = instruction_format(get_answer_prompt(question['question'], context, PROMPT_VERSION))
        instruction = get_answer_prompt(question['question'], context, PROMPT_VERSION)

        yield instruction


def get_all_answers(questions, path):
    counter = 0
    for response in generate_text(instruction_generator(questions)):
        question = questions[counter]
        question_id = question['id']
        raw_answer_path = f'{path}/{question_id}.txt'
        raw = response[0]['generated_text'].strip()
        print(f'Generated {question_id}: {raw}')

        raw_file = open(raw_answer_path, 'w')
        raw_file.write(raw)
        counter += 1


def get_answers(question, path):
    question_id = question['id']
    raw_answer_path = f'{path}/{question_id}.txt'

    if os.path.isfile(raw_answer_path):
        print(f'Skipping {question_id}: Already exists')
        return

    context = enumerate_lines(question['context'])
    instruction = instruction_format(get_answer_prompt(question['question'], context, PROMPT_VERSION))
    print(instruction)
    response = generate_text(instruction)
    raw = response[0]['generated_text'].strip()
    print(f'Generated {question_id}: {raw}')

    raw_file = open(raw_answer_path, 'w')
    raw_file.write(raw)


if __name__ == '__main__':
    languages = ['de', 'en']

    for language in languages:
        base_answer_path = f'../answers/{MODEL}/{PROMPT_VERSION}/{language}'
        answer_path = f'{base_answer_path}/{RAW_SLUG}'
        os.makedirs(answer_path, exist_ok=True)
        dataset_path = f'{DATASET_PATH}/{language}/dev_{language}.json'
        questions = json.load(open(dataset_path, 'r'))

        get_all_answers(questions, answer_path)

        postprocess_llm_answers(base_answer_path, questions)
