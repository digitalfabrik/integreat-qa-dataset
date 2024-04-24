MIXTRAL = 'mistralai/Mixtral-8x7B-Instruct-v0.1'
MISTRAL = 'mistralai/Mistral-7B-Instruct-v0.2'
LLAMA2 = 'meta-llama/Llama-2-7b-hf'
LLAMA3_8B = 'meta-llama/Llama-3-8B-Instruct'
LLAMA3_70B = 'meta-llama/Llama-3-70B-Instruct'
IGEL = 'instruct-igel-001'
GPT = 'gpt-3.5-turbo'
MODELS = [MIXTRAL, MISTRAL, LLAMA3_8B, LLAMA3_70B, IGEL, GPT]

PROMPT_v1 = 'v1'
PROMPT_v2 = 'v2'
PROMPTS = [PROMPT_v1, PROMPT_v2]

# Temperature = 0.75
RUN_0 = 0
RUN_1 = 1
RUNS = [RUN_0, RUN_1, 2]

CITY = 'rems-murr-kreis'
LANGUAGE = 'de'
MODEL = 'Mixtral-8x7B-Instruct-v0.1'

P_SELECTED_AGREEMENT = 0.03488382343589578

RESPONSES_SLUG = 'responses'
SUMMARIES_SLUG = 'summaries'
RAW_SLUG = 'raw'
READY_SLUG = 'ready'
PAGES_SLUG = 'pages'
BASE_SLUG = '../data'


def get_integreat_pages_json_path():
    return f'{BASE_SLUG}/integreat_pages/{CITY}/{LANGUAGE}/{PAGES_SLUG}.json'


def get_integreat_pages_path(slug):
    return f'{BASE_SLUG}/integreat_pages/{CITY}/{LANGUAGE}/{PAGES_SLUG}_no_h/{slug}'


def get_questions_with_evidence_path(slugs):
    return f'{BASE_SLUG}/questions_with_evidence_{MODEL}/{CITY}/{LANGUAGE}/{"/".join(slugs)}'


def get_questions_wo_evidence_path(slugs):
    return f'{BASE_SLUG}/questions_wo_evidence_{MODEL}/{CITY}/{LANGUAGE}/{"/".join(slugs)}'


def get_answers_path(slugs):
    return f'{BASE_SLUG}/answers_{MODEL}/{"/".join(slugs)}'


def get_dataset_path(extension, with_evidence=True):
    if with_evidence:
        return f'{BASE_SLUG}/questions_with_evidence_{MODEL}/dataset_{CITY}_{LANGUAGE}.{extension}'
    return f'{BASE_SLUG}/questions_wo_evidence_{MODEL}/dataset_wo_evidence_{CITY}_{LANGUAGE}.{extension}'


prompt_w_evidence_en = '''Give three simple and short one-part questions that can be answered with the users message.
The question should be specific and in easy-to-understand language.
Bad examples:
- What services are offered?
- How many people live in Germany?
- Does the user...?
Respond by giving the questions AND the answers.
For the answers, only give the line numbers, do not give whole sentences.
Good example:
"""
Q1: What language courses are available?
A1: 3, 4, 5
Q2: How can I find language courses?
A2: 7
Q3: What does language level B2 mean?
A3: 6
"""'''

prompt_w_evidence_de = '''Give three simple and short one-part questions that can be answered with the users message.
The question should be specific and in easy-to-understand German language.
Bad examples:
- Welche Dienstleistungen werden angeboten?
- Wie viele Menschen leben in Deutschland?
- Hat der Nutzer...?
Respond by giving the questions AND the answers.
For the answers, only give the line numbers, do not give whole sentences.
Good example:
"""
Q1: Welche Sprachkurse gibt es?
A1: 3, 4, 5
Q2: Wie kann ich Sprachkurse finden?
A2: 7
Q3: Was bedeutet das Sprachniveau B2?
A3: 6
"""'''

prompt_wo_evidence_en = '''You are a refugee/newcomer in Germany and are looking for help.
Give three simple and short one-part questions that could be answered by a text with the following topic.
The question should be specific and in easy-to-understand language.
Bad examples:
- What services are offered?
- How many people live in Germany?
- Does the user...?
Good example:
"""
Q1: What language courses are available?
Q2: How can I find language courses?
Q3: What does language level B2 mean?
"""'''

prompt_wo_evidence_de = ''''You are a refugee/newcomer in Germany and are looking for help.
Give three simple and short one-part questions that could be answered by a text with the following topic.
The question should be specific and in easy-to-understand German language.
Bad examples:
- Welche Dienstleistungen werden angeboten?
- Wie viele Menschen leben in Deutschland?
- Hat der Nutzer...?
Do NOT translate the questions or replicate previous messages..
Good example:
"""
Q1: Welche Sprachkurse gibt es?
Q2: Wie kann ich Sprachkurse finden?
Q3: Was bedeutet das Sprachniveau B2?
"""'''

prompt_summarize_en = 'Give the topic of the text using max. 3 words.'

prompt_summarize_de = 'Give the topic of the text using max. 3 words using German language.'


def get_prompt_answer_lines(text):
    return f'''
You are a helpful assistant trying to help refugees and newcomers in Germany to find answers to their questions in a given text.
Respond to the users question with ONLY the comma-separated line numbers of the answers in the following text.
If there is no answer in the text, respond with '-1'.
Do NOT add any text or explanation.
Bad examples:
- '3-5'
- '7,8 (the answer is not in the text)'
- 'The answers can be found in line 19 and 20'
Given Text:
"""{text}"""
'''


def get_prompt_format_w_answers(question, context):
    return f'''
Question: {question}

Context: {context}

Instruction: Given the question and context above, find the answer sentences to the question in the context.
Please use the format of: ## Answer: {{answer}} ## Numbers: {{comma separated sentence numbers}}
If there is no answer in the context, use the format of: ## Answer: None. ## Numbers: -1
'''


