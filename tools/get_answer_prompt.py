from constants import PROMPT_v1, PROMPT_v2


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


def get_answer_prompt(question, context, version):
    if version == PROMPT_v1:
        return v1(question, context)
    elif version == PROMPT_v2:
        return v2(question, context)
