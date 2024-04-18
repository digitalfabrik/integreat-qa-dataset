def v1(question, context):
    return f'''
Question: {question}

Context: {context}

Instruction: Given the question and context above, find the answer sentences to the question in the context.
Please use the format of: ## Answer: {{answer}} ## Numbers: {{comma separated sentence numbers}}
If there is no answer in the context, use the format of: ## Answer: None. ## Numbers: -1
'''


def get_answer_prompt(question, context, version):
    if version == 'v1':
        return v1(question, context)
