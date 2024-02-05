import os
import os.path
from constants import get_integreat_pages_path, get_questions_with_evidence_path, RAW_SLUG, RESPONSES_SLUG, LANGUAGE, prompt_w_evidence_de, prompt_w_evidence_en
from llama_cpp import Llama

MODEL = '/hpc/gpfs2/scratch/u/kleinlst/thesis/integreat-chat-dataset/models/mixtral-8x7b-instruct-v0.1.Q5_K_M.gguf'
llm = Llama(model_path=MODEL, chat_format="llama-2", n_threads=8, n_ctx=6144)


# Add line numbers to each line
def enumerate_lines(text):
    lines = text.split('\n')
    numerated_lines = []
    for index, line in enumerate(lines):
        numerated_lines.append(str(index) + ' ' + line)

    return '\n'.join(numerated_lines)


def generate_questions(slug):
    page_path = get_integreat_pages_path(slug)
    raw_path = get_questions_with_evidence_path([RAW_SLUG, slug])
    response_path = get_questions_with_evidence_path([RESPONSES_SLUG, slug])

    if os.path.isfile(response_path):
        print(f'Skipping {slug}: Already exists')
        return

    page_file = open(page_path, 'r')
    content = page_file.read()

    if ('The service is free' in content) or ('Das Angebot ist kostenfrei' in content):
        # Questions about pages with specific services are most of the time things like 'Is the service free?'
        print(f'Skipping {slug}: Specific service')
        return

    if len(content) > 5000:
        # Max context length in the backend is 5000 chars
        print(f'Skipping {slug}: Context too long')
        return

    response = llm.create_chat_completion(
        messages=[
            {'role': 'system', 'content': prompt_w_evidence_de if LANGUAGE == 'de' else prompt_w_evidence_en},
            {'role': 'user', 'content': enumerate_lines(content)},
        ]
    )

    raw = response['choices'][0]['message']['content']
    raw_file = open(raw_path, 'w')
    raw_file.write(raw)
    print(f'Generated {slug}: {raw}')

    response_file = open(response_path, 'w')
    response_file.write(str(response))


if __name__ == '__main__':
    os.makedirs(get_questions_with_evidence_path([RAW_SLUG]), exist_ok=True)
    os.makedirs(get_questions_with_evidence_path([RESPONSES_SLUG]), exist_ok=True)

    page_path = get_integreat_pages_path('')
    slugs = os.listdir(page_path)

    for slug in slugs:
        generate_questions(slug)
