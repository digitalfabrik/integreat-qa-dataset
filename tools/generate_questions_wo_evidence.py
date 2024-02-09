import os
import os.path
from constants import get_integreat_pages_path, get_questions_wo_evidence_path, RAW_SLUG, SUMMARIES_SLUG, \
    prompt_wo_evidence_en, LANGUAGE, prompt_wo_evidence_de
from transformers import pipeline
from torch import bfloat16

MODEL = '/hpc/gpfs2/scratch/g/coling/models/mistralai/Mixtral-8x7B-Instruct-v0.1'

generate_text = pipeline(
    'text-generation',
    model=MODEL,
    return_full_text=False,
    torch_dtype=bfloat16,
    device_map='auto',
    max_new_tokens=512
)


def instruction_format(instructions, query):
    return f'<s> [INST] {instructions} [/INST\nUser: {query}]\nAssistant: '


# Add line numbers to each line
def enumerate_lines(text):
    lines = text.split('\n')
    numerated_lines = []
    for index, line in enumerate(lines):
        numerated_lines.append(str(index) + ' ' + line)

    return '\n'.join(numerated_lines)


def summarize(slug):
    page_path = get_integreat_pages_path(slug)
    summary_path = get_questions_wo_evidence_path([SUMMARIES_SLUG, slug])
    raw_path = get_questions_wo_evidence_path([RAW_SLUG, slug])

    if os.path.isfile(raw_path):
        print(f'Skipping {slug}: Already exists')
        return

    page_file = open(page_path, 'r')
    content = page_file.read()

    if ('The service is free' in content) or ('Das Angebot ist kostenfrei' in content):
        # Questions about pages with specific services are most of the time things like 'Is the service free?'
        # print(f'Skipping {slug}: Specific service')
        return

    if len(content) > 8000:
        # Max context length in the backend is 8000 chars
        print(f'Skipping {slug}: Context too long')
        return

    summary_response = generate_text(instruction_format(
        'Give the topic of the text using max. 3 words.',
        enumerate_lines(content)
    ))
    summary = summary_response[0]['generated_text'].strip()
    print(f'Summarized {slug}: {summary}')

    summary_file = open(summary_path, 'w')
    summary_file.write(summary)

    response = generate_text(instruction_format(
        prompt_wo_evidence_de if LANGUAGE == 'de' else prompt_wo_evidence_en,
        summary
    ))
    raw = response[0]['generated_text'].strip()
    print(f'Generated {slug}: {raw}')

    raw_file = open(raw_path, 'w')
    raw_file.write(raw)


if __name__ == '__main__':
    os.makedirs(get_questions_wo_evidence_path([RAW_SLUG]), exist_ok=True)
    os.makedirs(get_questions_wo_evidence_path([SUMMARIES_SLUG]), exist_ok=True)

    page_path = get_integreat_pages_path('')
    slugs = os.listdir(page_path)

    for slug in slugs:
        summarize(slug)
