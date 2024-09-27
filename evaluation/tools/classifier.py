import json
import numpy as np
import evaluate
import pandas as pd
from datasets import Dataset

from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer, \
    DataCollatorWithPadding, EarlyStoppingCallback

BERT = 'google-bert/bert-base-uncased'
DEBERTA = 'deberta-v3-large'
model_name = DEBERTA

language = 'de'
CONTEXT_WINDOW = 5
SENTENCE_LEVEL = True
max_length = (CONTEXT_WINDOW * 2 + 2) * 32

MODEL_PATH = f'/hpc/gpfs2/scratch/g/coling/models/{model_name}'
# MODEL_PATH = f'/home/st/Downloads/{model_name}'

id2label = {0: 'NO', 1: 'YES'}
label2id = {'NO': 0, 'YES': 1}

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, do_lower_case=True, additional_special_tokens=['[SEN]'])
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH, num_labels=2, id2label=id2label, label2id=label2id)
base_dir = f'/hpc/gpfs2/scratch/u/kleinlst/thesis/integreat-qa-dataset/train/{model_name}/{'answers' if SENTENCE_LEVEL else 'unanswerable'}/{language}'
output_dir = f'{base_dir}/{f"context_{CONTEXT_WINDOW}_" if SENTENCE_LEVEL else ""}standard'
training_arguments = TrainingArguments(
    output_dir=output_dir,
    evaluation_strategy='steps',
    save_strategy='steps',
    eval_steps=50 if SENTENCE_LEVEL else 10,
    learning_rate=2e-6,
    num_train_epochs=3 if SENTENCE_LEVEL else 10,
    weight_decay=0.1,
    do_train=True,
    do_eval=True,
    disable_tqdm=True,
    load_best_model_at_end=True,
    metric_for_best_model='f1',
    warmup_steps=50,
)
f1 = evaluate.load('/hpc/gpfs2/scratch/u/kleinlst/thesis/integreat-qa-dataset/evaluate/metrics/f1')
precision = evaluate.load('/hpc/gpfs2/scratch/u/kleinlst/thesis/integreat-qa-dataset/evaluate/metrics/precision')
recall = evaluate.load('/hpc/gpfs2/scratch/u/kleinlst/thesis/integreat-qa-dataset/evaluate/metrics/recall')
accuracy = evaluate.load('/hpc/gpfs2/scratch/u/kleinlst/thesis/integreat-qa-dataset/evaluate/metrics/accuracy')
iou = evaluate.load('/hpc/gpfs2/scratch/u/kleinlst/thesis/integreat-qa-dataset/evaluate/metrics/mean_iou')


def tokenize(data):
    if SENTENCE_LEVEL:
        return tokenizer(data['question'], data['context'], truncation=True)
    else:
        return tokenizer(data['text'], truncation=True, max_length=1024)


def prepare_split(path):
    split = json.load(open(path, 'r'))
    data = []
    for row in split:
        context = row['context']
        answers = row['answers']
        question = row['question']

        if SENTENCE_LEVEL:
            sentences = context.split('\n')
            for index, sentence in enumerate(sentences):
                previous = ' '.join(sentences[max(0, index - CONTEXT_WINDOW):index])
                next = ' '.join(sentences[index + 1:index + CONTEXT_WINDOW + 1])
                context = f'{previous}[SEN]{sentence}[SEN]{next}' if CONTEXT_WINDOW > 0 else sentence
                data.append({'question': question, 'context': context, 'label': 1 if index in answers else 0})
        else:
            data.append({'text': f'[CLS]{question}[SEP]{context}[SEP]', 'label': 1 if len(answers) == 0 else 0})

    return Dataset.from_pandas(pd.DataFrame(data)).map(tokenize, batched=True), split


def load_splits(language):
    train = prepare_split(f'../datasets/splits/{language}/train_{language}.json')
    dev = prepare_split(f'../datasets/splits/{language}/dev_{language}.json')
    test = prepare_split(f'../datasets/splits/{language}/test_{language}.json')
    return train[0], dev[0], test[0], train[1], dev[1], test[1]


def compute_metrics(evaluation_prediction):
    logits, labels = evaluation_prediction
    predictions = np.argmax(logits, axis=1)
    a = accuracy.compute(predictions=predictions, references=labels)
    r = recall.compute(predictions=predictions, references=labels)
    p = precision.compute(predictions=predictions, references=labels)
    f = f1.compute(predictions=predictions, references=labels)
    return {"f1": f['f1'], "precision": p['precision'], "recall": r['recall'], "accuracy": a['accuracy']}


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


if __name__ == '__main__':
    train, dev, test, _train, _dev, _test = load_splits(language)
    print(train)
    print(len(train), len(dev), len(test))
    print(model)
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    trainer = Trainer(
        args=training_arguments,
        model=model,
        train_dataset=train,
        eval_dataset=dev,
        compute_metrics=compute_metrics,
        tokenizer=tokenizer,
        data_collator=data_collator,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=10)]
    )
    trainer.train()
    trainer.save_model(output_dir)
    predictions = trainer.predict(test)
    predicted_labels = np.argmax(predictions.predictions, axis=1)
    print(output_dir.split('/train/')[1])
    print(predictions.metrics)
    file = open(f'{output_dir}/predicted.json', 'w')
    predicted = {}
    if SENTENCE_LEVEL:
        current_index = 0
        for index, row in enumerate(_test):
            answer_lines = []
            sentence_count = len(row['context'].split('\n'))
            for i in range(current_index, current_index + sentence_count):
                if predicted_labels[i] == 1:
                    answer_lines.append(i - current_index)
            predicted[row['id']] = answer_lines
            current_index += sentence_count
    else:
        for index, row in enumerate(_test):
            predicted[row['id']] = bool(predicted_labels[index] == 1)
    print(predicted)
    file.write(json.dumps(predicted))
    file = open(f'{output_dir}/prediction.json', 'w')
    file.write(json.dumps(predictions.predictions, cls=NumpyEncoder))
    file = open(f'{output_dir}/labels.json', 'w')
    file.write(json.dumps(predictions.label_ids, cls=NumpyEncoder))
    file = open(f'{output_dir}/metrics.json', 'w')
    file.write(json.dumps(predictions.metrics))
