export type Annotation = {
  answerLines: number[]
  noAnswer: boolean
  comment: string
  user?: string
}

export type Question = {
  id: number
  pageId: number
  pagePath: string
  context: string
  question: string
  answerLines: number[]
  noAnswer: boolean
  comment: string
  city: string
  language: string
  annotations: Annotation[]
}

export type RowJson = {
  pageId: number
  pagePath: string
  city: string
  language: string
  context: string
  questions: {
    question: string
    answerLines: number[]
    annotations: {
      comment: string
      answerLines: number[]
      noAnswer: boolean
      user: string
    }[]
  }[]
}

export type QuestionJson = {
  id: number
  value: RowJson
}

export const mapRowsToQuestions = (json: RowJson[]): Question[] =>
  json.reduce(
    (acc: Question[], row: RowJson): Question[] => [
      ...acc,
      ...row.questions.map((it, index) => ({
        id: index,
        pageId: row.pageId,
        pagePath: row.pagePath,
        context: row.context,
        city: row.city,
        language: row.language,
        question: it.question,
        annotations: it.annotations,
        answerLines: [],
        noAnswer: false,
        comment: '',
      })),
    ],
    [],
  )

const mapToQuestion = (json: QuestionJson, index = 0): Question => ({
  id: json.id,
  pageId: json.value.pageId,
  pagePath: json.value.pagePath,
  context: json.value.context,
  city: json.value.city,
  language: json.value.language,
  question: json.value.questions[index].question,
  annotations: json.value.questions[index].annotations,
  answerLines: [],
  noAnswer: false,
  comment: '',
})

export default mapToQuestion
