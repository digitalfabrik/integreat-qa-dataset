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
}

export type QuestionJson = {
  id: number
  value: {
    pageId: number
    pagePath: string
    city: string
    language: string
    context: string
    questions: {
      question: string
      answerLines: number[]
    }[]
  }
}

const mapToQuestion = (json: QuestionJson): Question => ({
  id: json.id,
  pageId: json.value.pageId,
  pagePath: json.value.pagePath,
  context: json.value.context,
  city: json.value.city,
  language: json.value.language,
  question: json.value.questions[0].question,
  answerLines: [],
  noAnswer: false,
  comment: '',
})

export default mapToQuestion
