![Integreat](integreat.svg)

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://choosealicense.com/licenses/mit/)
[![GitHub license](https://img.shields.io/badge/license-CC_BY-blue.svg)](https://creativecommons.org/licenses/by/4.0/)

# OMoS - Extractive QA Dataset for Integreat

This repository contains our [**integreat-qa-omos** dataset](#dataset).
The dataset contains German and English questions in a German migration context with contexts taken from the [Integreat-App](https://github.com/digitalfabrik/integreat-app), an open-source and multilingual integration platform.

This repository also contains a web-based [annotation tool](#annotation-tool) to facilitate the manual extraction of answer sentences.
Furthermore, we evaluate different approaches and models on our dataset.

## Contents

- [Dataset](#dataset): Our dataset for QA in Integreat
- [Annotation Tool](#annotation-tool): A web-based annotation tool for answer sentence extraction
- [Evaluation](evaluation): Evaluation of LLMs and encoder-only models on the integreat-qa-omos dataset 

## Dataset

Our dataset consists of 906 diverse QA pairs in German and English.
The dataset is extractive, i.e., answers are given as sentence indices (breaking at the newline character `\n`).
Questions are automatically generated using an LLM.
The answers are manually annotated using voluntary crowdsourcing.

Our dataset is licensed under [cc-by-4.0](https://choosealicense.com/licenses/cc-by-4.0).
The dataset is also available on [hugging face](https://huggingface.co/datasets/digitalfabrik/integreat-qa-omos).

### Properties

A QA pair consists of
- `question` (string): Question
- `context` (string): Full text from the Integreat-App
- `answers` (number[]): Indices of answer sentences

Furthermore, the following properties are present:
- `language` (string): The language of question and context.
- `sourceLanguage` (string | null): If question and context are machine translated, the source language.
- `city` (string): The city the page in the Integreat-App belongs to.
- `pageId` (number): The page id of the page in the Integreat-App.
- `jaccard` (number): The sentence-level inter-annotator agreement of manual answer annotation.

### Dataset Construction

An overview of the dataset construction can be seen here:
![dataset-construction](resources/dataset-construction.svg)

#### Question Generation

We generated questions automatically using two different approaches:
Prompting the model with the whole context and prompting with just a short three-word topic summary.

![dataset-construction](resources/question-generation.svg)

#### Answer Annotation

Our answer annotations are done manually by voluntary crowdsourcing using our web-based [annotation tool](#annotation-tool).
In order to guarantee high-quality annotations, we require two annotations per question.
Only questions with high inter-annotator agreement are present in our dataset.

## Annotation Tool

In order to facilitate the manual answer annotation, we created our own web-based annotation tool which can be found in [annotation-tool](annotation-tool).
The annotation tools consists of two components:
- A React [frontend](annotation-tool/frontend) written in TypeScript
- A Ktor [backend](annotation-tool/backend) written in Kotlin

<p float="left">
<img src="resources/annotation_tool_answerable.png" width="49%" />
<img src="resources/annotation_tool_unanswerable.png" width="49%" />
</p>
