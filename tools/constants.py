CITY = 'muenchen'
LANGUAGE = 'de'
MODEL = 'mixtral-8x7B-Instruct-v0.1.Q5_K_M.gguf'

RESPONSES_SLUG = 'responses'
RAW_SLUG = 'raw'
READY_SLUG = 'ready'
PAGES_SLUG = 'pages'
BASE_SLUG = '../data'


def get_integreat_pages_json_path():
    return f'{BASE_SLUG}/integreat_pages/{CITY}/{LANGUAGE}/{PAGES_SLUG}.json'


def get_integreat_pages_path(slug):
    return f'{BASE_SLUG}/integreat_pages/{CITY}/{LANGUAGE}/{PAGES_SLUG}/{slug}'


def get_questions_with_evidence_path(slugs):
    return f'{BASE_SLUG}/questions_with_evidence_{MODEL}/{CITY}/{LANGUAGE}/{"/".join(slugs)}'


prompt_w_evidence_en = f'''Give three simple and short one-part questions that can be answered with the users message.
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


prompt_w_evidence_de = f'''Give three simple and short one-part questions that can be answered with the users message.
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
