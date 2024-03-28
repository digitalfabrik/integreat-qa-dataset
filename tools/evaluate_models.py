import json
import datetime
import os

from transformers import pipeline


model_name = "roberta-base-squad2"
full_model_name = f'deepset/{model_name}'
DATASET_PATH = f'../datasets/{datetime.datetime.utcnow().date().isoformat()}_dataset_en.json'
PREDICTIONS_PATH = f'predictions/{model_name}_predictions.json'

if __name__ == '__main__':
    questions = json.load(open(DATASET_PATH, 'r'))
    predictions = []

    if os.path.exists(PREDICTIONS_PATH, ):
        predictions = json.load(open(PREDICTIONS_PATH, 'r'))
    else:
        nlp = pipeline('question-answering', model=full_model_name, tokenizer=full_model_name)
        qa_input = [{'question': question['question'], 'context': question['context']} for question in questions]
        predictions = nlp(qa_input)
        predictions_file = open(PREDICTIONS_PATH, 'w')
        predictions_file.write(json.dumps(predictions))

    correct_answer = 0
    answer_count = 0
    correct_no_answer = 0
    no_answer = 0

    for index, prediction in enumerate(predictions):
        question = questions[index]

        if prediction['score'] > 0.8:
            answer_count += 1
            # Answer found
            lines = question['context'].split('\n')
            answer = ' '.join([lines[line] for line in question['answers']])
            print(question['question'], prediction['answer'], ' | ', answer, ' | ', prediction['score'])
            predicted_line_number = question['context'][:prediction['start']].count('\n')
            predicted_in_annotated = predicted_line_number in question['answers']
            if predicted_in_annotated:
                correct_answer += 1
        else:
            no_answer += 1
            if len(question['answers']) == 0:
                correct_no_answer += 1

    print(correct_answer, answer_count, correct_answer / answer_count)
    print(correct_no_answer, no_answer, correct_no_answer / no_answer)
    print((correct_answer + correct_no_answer) / len(questions))
