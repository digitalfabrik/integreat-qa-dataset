import json
import numpy as np
import evaluate
import pandas as pd
from datasets import Dataset

from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer

MAX_LEN = 512
model_name = 'google-bert/bert-base-uncased'

tokenizer = AutoTokenizer.from_pretrained(model_name, do_lower_case=True)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)
training_arguments = TrainingArguments(output_dir=f'{model_name}_train', evaluation_strategy='epoch')
metric = evaluate.load('precision')


def tokenize(data):
    return tokenizer(data['text'], padding='max_length', truncation=True)


def prepare_split(path):
    split = json.load(open(path, 'r'))
    data = []
    for row in split:
        context = row['context']
        answers = row['answers']
        question = row['question']
        for index, sentence in enumerate(context.split('\n')):
            data.append({'text': f'{question} {sentence}', 'label': 1 if index in answers else 0})

    return Dataset.from_pandas(pd.DataFrame(data)).map(tokenize, batched=True)


def load_splits(language):
    train = prepare_split(f'../datasets/splits/{language}/train_{language}.json')
    dev = prepare_split(f'../datasets/splits/{language}/dev_{language}.json')
    test = prepare_split(f'../datasets/splits/{language}/test_{language}.json')
    return train, dev, test


def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)


if __name__ == '__main__':
    language = 'en'
    train, dev, test = load_splits(language)

    trainer = Trainer(
        model=model,
        args=training_arguments,
        train_dataset=train,
        eval_dataset=dev,
        compute_metrics=compute_metrics,
    )
    trainer.train()
