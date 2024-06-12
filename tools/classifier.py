import json
import numpy as np
import evaluate
import pandas as pd
from datasets import Dataset

from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer, DataCollatorWithPadding, pipeline
BERT = 'google-bert/bert-base-uncased'
DEBERTA = 'deberta-v3-large'
model_name = DEBERTA

max_length = 512

MODEL_PATH = f'/hpc/gpfs2/scratch/g/coling/models/{model_name}'

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, do_lower_case=True)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH, num_labels=2)
output_dir=f'/hpc/gpfs2/scratch/u/kleinlst/thesis/integreat-qa-dataset/train/{model_name}'
training_arguments = TrainingArguments(
    output_dir=output_dir,
    evaluation_strategy='steps',
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01,
    save_strategy="epoch",
    load_best_model_at_end=True,
    do_train=True,
)
metric = evaluate.load('/hpc/gpfs2/scratch/u/kleinlst/thesis/integreat-qa-dataset/evaluate/metrics/f1')


def tokenize(data):
    return tokenizer(data['text'], padding='max_length', truncation=True, max_length=max_length)


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
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    trainer = Trainer(
        model=model,
        args=training_arguments,
        train_dataset=train,
        eval_dataset=dev,
        compute_metrics=compute_metrics,
        tokenizer=tokenizer,
        data_collator=data_collator
    )
    trainer.train()

    classifier = pipeline("text-classification", model="stevhliu/my_awesome_model")
    for instance in test:
        instance.
        classifier(text)
        [{'label': 'POSITIVE', 'score': 0.9994940757751465}]