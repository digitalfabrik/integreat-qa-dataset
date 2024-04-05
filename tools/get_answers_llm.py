import json
import os
import os.path

from constants import RAW_SLUG, get_answers_path, get_prompt_format_w_answers
from transformers import pipeline
from torch import bfloat16

MODEL = '/hpc/gpfs2/scratch/g/coling/models/mistralai/Mixtral-8x7B-Instruct-v0.1'
DATASET_PATH = f'/hpc/gpfs2/scratch/u/kleinlst/thesis/integreat-chat-dataset/datasets/2024-04-01_dataset.json'

generate_text = pipeline(
    'text-generation',
    model=MODEL,
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


def get_answers(question):
    question_id = question['id']
    raw_answer_path = get_answers_path(['format_w_sentences', RAW_SLUG, f'{question_id}.txt'])

    if os.path.isfile(raw_answer_path):
        print(f'Skipping {question_id}: Already exists')
        return

    context = enumerate_lines(question['context'])
    instruction = instruction_format(get_prompt_format_w_answers(question['question'], context))
    print(instruction)
    response = generate_text(instruction)
    raw = response[0]['generated_text'].strip()
    print(f'Generated {question_id}: {raw}')

    raw_file = open(raw_answer_path, 'w')
    raw_file.write(raw)


if __name__ == '__main__':
    os.makedirs(get_answers_path(['format_w_sentences', RAW_SLUG]), exist_ok=True)
    questions = json.load(open(DATASET_PATH, 'r'))

    for question in questions:
        get_answers(question)

