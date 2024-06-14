import json
import numpy as np
import evaluate
import pandas as pd
from datasets import Dataset

from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer, \
    DataCollatorWithPadding

BERT = 'google-bert/bert-base-uncased'
DEBERTA = 'deberta-v3-large'
model_name = DEBERTA

language = 'en'
CONTEXT_WINDOW = 4
max_length = (CONTEXT_WINDOW * 2 + 2) * 32

MODEL_PATH = f'/hpc/gpfs2/scratch/g/coling/models/{model_name}'

id2label = {0: 'NO', 1: 'YES'}
label2id = {'NO': 0, 'YES': 1}

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, do_lower_case=True, additional_special_tokens=['[SEN]'])
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH, num_labels=2, id2label=id2label, label2id=label2id)
output_dir = f'/hpc/gpfs2/scratch/u/kleinlst/thesis/integreat-qa-dataset/train/{model_name}_context_{CONTEXT_WINDOW}_{language}'
training_arguments = TrainingArguments(
    output_dir=output_dir,
    evaluation_strategy='steps',
    save_strategy='steps',
    eval_steps=500,
    learning_rate=2e-5,
    num_train_epochs=10,
    weight_decay=0.1,
    do_train=True,
    do_eval=True,
    disable_tqdm=True
)
f1 = evaluate.load('/hpc/gpfs2/scratch/u/kleinlst/thesis/integreat-qa-dataset/evaluate/metrics/f1')
precision = evaluate.load('/hpc/gpfs2/scratch/u/kleinlst/thesis/integreat-qa-dataset/evaluate/metrics/precision')
recall = evaluate.load('/hpc/gpfs2/scratch/u/kleinlst/thesis/integreat-qa-dataset/evaluate/metrics/recall')
accuracy = evaluate.load('/hpc/gpfs2/scratch/u/kleinlst/thesis/integreat-qa-dataset/evaluate/metrics/accuracy')
iou = evaluate.load('/hpc/gpfs2/scratch/u/kleinlst/thesis/integreat-qa-dataset/evaluate/metrics/mean_iou')


def tokenize(data):
    return tokenizer(data['question'], data['context'], truncation=True)


def prepare_split(path):
    split = json.load(open(path, 'r'))
    data = []
    for row in split:
        context = row['context']
        answers = row['answers']
        question = row['question']

        sentences = context.split('\n')
        for index, sentence in enumerate(sentences):
            previous = ' '.join(sentences[max(0, index - CONTEXT_WINDOW):index])
            next = ' '.join(sentences[index + 1:index + CONTEXT_WINDOW + 1])
            context = f'{previous}[SEN]{sentence}[SEN]{next}' if CONTEXT_WINDOW > 0 else sentence
            data.append({'question': question, 'context': context, 'label': 1 if index in answers else 0})

    return Dataset.from_pandas(pd.DataFrame(data)).map(tokenize, batched=True)


def load_splits(language):
    train = prepare_split(f'../datasets/splits/{language}/train_{language}.json')
    dev = prepare_split(f'../datasets/splits/{language}/dev_{language}.json')
    test = prepare_split(f'../datasets/splits/{language}/test_{language}.json')
    return train, dev, test


def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=1)
    return f1.compute(predictions=predictions, references=labels)


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


if __name__ == '__main__':
    train, dev, test = load_splits(language)
    print(train)
    print(len(train))
    print(f'{model} with context length {CONTEXT_WINDOW}')
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    trainer = Trainer(
        args=training_arguments,
        model=model,
        train_dataset=train,
        eval_dataset=dev,
        compute_metrics=compute_metrics,
        tokenizer=tokenizer,
        data_collator=data_collator
    )
    trainer.train()
    trainer.save_model(output_dir)
    predictions = trainer.predict(test)
    print(predictions)
    file = open(f'{output_dir}/prediction.json', 'w')
    file.write(json.dumps(predictions.predictions, cls=NumpyEncoder))
    file = open(f'{output_dir}/labels.json', 'w')
    file.write(json.dumps(predictions.label_ids, cls=NumpyEncoder))
    file = open(f'{output_dir}/metrics.json', 'w')
    file.write(json.dumps(predictions.metrics))
