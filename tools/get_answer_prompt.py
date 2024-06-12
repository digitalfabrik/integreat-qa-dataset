import json

from constants import PROMPT_v1, PROMPT_v2, PROMPT_v3, PROMPT_v4

def v1(question, context):
    return f'''
Question: {question}

Context: {context}

Instruction: Given the question and context above, find the answer sentences to the question in the context.
Please use the format of: ## Answer: {{answer}} ## Numbers: {{answer sentence numbers}}
If there is no answer in the context, use the format of: ## Answer: None. ## Numbers: -1
'''


def v2(question, context):
    return f'''
Given the question and context below, find the answer sentences to the question in the context.
Please use the format of: ## Answer: {{answer}} ## Sentence numbers: {{answer sentence numbers}}
If there is no answer in the context, use the format of: ## Answer: None. ## Numbers: -1

Question: {question}

Context: {context}
'''


few_shot_examples_de = [
    {
        'id': 65,
        'question': 'Was braucht man, um ein Bankkonto zu eröffnen?',
        'answers': [],
        'context': '[9] Ab wann darf ich Auto fahren lernen?\n[10] In Deutschland darf man nur mit einem gültigen Führerschein »» Auto fahren.\n[11] Vorher muss man eine Fahrschule besuchen und theoretische und praktische Unterrichtsstunden nehmen, die man auch bezahlen muss.\n[12] Informationen dazu bekommst du in der Fahrschule.\n[13] Wann darf ich ein eigenes Bankkonto eröffnen?'
    },
    {
        'id': 207,
        'question': 'Was ist eine Fiktionsbescheinigung?',
        'answers': [2],
        'context': '[0] Aufenthalt mit Fiktionsbescheinigung\n[1] Ausreise mit einer Fiktionsbescheinigung\n[2] Mit einer Fiktionsbescheinigung haben Sie ein vorläufiges Aufenthaltsrecht.\n[3] Es gibt verschiedene Arten einer Fiktionsbescheinigung.\n[4] Bitte beachten Sie:\n[5] Eine Wiedereinreise in das Bundesgebiet ist nur mit einer Fiktionsbescheinigung nach § 81 Abs.4 AufenthG möglich.'
    },
    {
        'id': 13,
        'question': 'Wo kann man Informationen zu den Aufnahmeverfahren an Berufsfachschulen finden?',
        'answers': [14, 15],
        'context': '[11] Die berufliche Erstausbildung ist an Berufsschulen und Berufsfachschulen möglich.\n[12] Die Ausbildung kann sowohl im»» Dualen System (Ausbildungsbetrieb und Besuch der Berufsschule) als auch durch eine rein»» schulische Ausbildung (Berufsfachschulen) erfolgen.\n[13] Die Termine und Anmeldevoraussetzungen sind bei den jeweiligen beruflichen Schulen unterschiedlich.\n[14] Vor der Einschreibung finden an Berufsfachschulen jedes Jahr Informationsabende statt.\n[15] Informationen zum Aufnahmeverfahren an den Berufsfachschulen erhalten Sie direkt bei der jeweiligen Schule.'
    },
    {
        'id': 3241,
        'question': 'Welche Schularten gibt es in Deutschland?',
        'answers': [],
        'context': '[0] Unterstützung bei schulischen oder persönlichen Problemen\n[1] Dein Kind benötigt Hilfe bei Problemen?\n[2] Dann helfen Dir diese Stellen:\n[3] Jugendsozialarbeit (kurz: JaS) und Jugendarbeit an Schulen (kurz: JA) bei schulischen, persönlichen oder familiären Problemen:\n[4] Am besten wendest Du Dich direkt an die Schule oder für generelle Informationen an das Landratsamt Augsburg:'
    },
    {
        'id': 349,
        'question': 'Welche Themen werden in den Erstorientierungskursen behandelt?',
        'answers': [2, 4, 5, 6],
        'context': '[2] Die Deutschkurse zur sprachlichen Erstorientierung (auch: Erstorientierungskurse) vermitteln sowohl elementare Deutschkenntnisse als auch Informationen über das Leben in Deutschland.\n[3] Sie sind eine praktische Starthilfe im neuen Lebensumfeld und erleichtern die Orientierung im Alltag.\n[4] Ein Kurs umfasst 300 Unterrichtseinheiten mit jeweils 45 Minuten und behandelt Themen wie „Gesundheit/Medizinische Versorgung“, „Arbeit“, „Kindergarten/Schule“, „Wohnen“, „Orientierung vor Ort/Verkehr/Mobilität“.\n[5] Im Fokus steht die mündliche Kommunikation: Die Teilnehmerinnen und Teilnehmer sollen so schnell wie möglich lernen, sich im Alltag zurechtzufinden.\n[6]Modulübergreifend geht es bei Erstorientierungskursen auch um die Vermittlung von Werten.'
    }
]

few_shot_examples_en = [
    {
        'id': 65,
        'question': 'What do you need to open a bank account?',
        'answers': [],
        'context': '[9] When can I start learning to drive?\n[10] In Germany, you may only drive a car with a valid driver\'s license "".\n[11] Beforehand, you have to attend a driving school and take theoretical and practical lessons, which you also have to pay for.\n[12] You can get information about this at the driving school.\n[13] When can I open my own bank account?',
    },
    {
        'id': 207,
        'question': 'What is a fictitious certificate?',
        'answers': [2],
        'context': '[0] Residence with fictitious certificate\n[1] Departure with a fictitious certificate\n[2] With a fictitious certificate, you have a temporary right of residence.\n[3] There are different types of fictitious certificate.\n[4]Please note:\n[5] Re-entry into the federal territory is only possible with a fictitious certificate in accordance with § 81 para.4 AufenthG possible.',
    },
    {
        'id': 13,
        'question': 'Where can I find information on admission procedures at vocational schools?',
        'answers': [14, 15],
        'context': '[11] Initial vocational training is possible at vocational schools and vocational colleges.\n[12] Training can take place both in the"" dual system (training company and vocational school) or "purely"" school-based training (vocational schools).\n[13] The dates and registration requirements vary from vocational school to vocational school.\n[14] Information evenings are held at vocational schools every year before enrollment.\n[15] Information on the admission procedure at the vocational schools can be obtained directly from the respective school.',
    },
    {
        'id': 3241,
        'question': 'What types of school are there in Germany?',
        'answers': [],
        'context': '[0] Support with school or personal problems\n[1] Does your child need help with problems?\n[2] Then these places will help you:\n[3] Youth social work (JaS for short) and youth work at schools (JA for short) for school, personal or family problems:\n[4] It is best to contact the school directly or the Augsburg District Office for general information:',
    },
    {
        'id': 349,
        'question': 'What topics are covered in the initial orientation courses?',
        'answers': [2, 4, 5, 6],
        'context': '[2] The German courses for initial language orientation (also known as initial orientation courses) teach both basic German language skills and information about life in Germany.\n[3] They are a practical starting aid in the new living environment and make everyday life easier.\n[4] A course comprises 300 teaching units of 45 minutes each and covers topics such as "Health/medical care", "Work", "Kindergarten/school", "Housing", "Local orientation/transport/mobility".\n[5] The focus is on oral communication: participants should learn as quickly as possible to find their way around in everyday life.\n[6] Across all modules, initial orientation courses are also about teaching values.',
    }
]


def v3_user(question, context):
    return {'role': 'user', 'content': f'''Given the question and document below, select the sentences from the document that answer the question.
It may also be the case that none of the sentences answers the question.
In the document, each sentence is marked with an ID.
Output the IDs of the relevant sentences as a list, e.g., "[1,2,3]", and output "[]" if no sentence is relevant.
Output only these lists.

Question: {question}

Document: {context}
'''}


def v3_assistant(answers):
    return {'role': 'assistant', 'content': json.dumps(answers)}


def v3(question, context, language, num_shots=5):
    messages = [{'role': 'system', 'content': 'Your task is to select sentences from a document that answer a given question.'}]
    shots = few_shot_examples_de if language == 'de' else few_shot_examples_en
    for shot in shots[:num_shots]:
        messages.append(v3_user(shot['question'], shot['context']))
        messages.append(v3_assistant(shot['answers']))
    messages.append(v3_user(question, context))
    return messages


def get_answer_prompt(question, context, version, language='de'):
    if version == PROMPT_v1:
        return v1(question, context)
    elif version == PROMPT_v2:
        return [{'role': 'user', 'content': v2(question, context)}]
    elif version == PROMPT_v3:
        return v3(question, context, language)
    elif version == PROMPT_v4:
        return v3(question, context, language, 0)


