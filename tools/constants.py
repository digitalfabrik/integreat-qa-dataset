CITY = 'muenchen'
LANGUAGE = 'de'

RESPONSES_SLUG = 'responses'
RAW_SLUG = 'raw'
PAGES_SLUG = 'pages'
BASE_SLUG = '../data'


def get_integreat_pages_json_path():
    return f'{BASE_SLUG}/integreat_pages/{CITY}/{LANGUAGE}/{PAGES_SLUG}.json'


def get_integreat_pages_path(slug):
    return f'{BASE_SLUG}/integreat_pages/{CITY}/{LANGUAGE}/{PAGES_SLUG}/{slug}'


def get_questions_with_evidence_path(slugs):
    return f'{BASE_SLUG}/questions_with_evidence/{CITY}/{LANGUAGE}/{"/".join(slugs)}'
