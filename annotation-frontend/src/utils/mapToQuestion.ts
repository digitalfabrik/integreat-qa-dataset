export type Question = {
  id: number
  pageId: number
  context: string
  question: string
  answerLines: number[]
  poor: boolean
  city: string
  language: string
}

type QuestionJson = {
  id: number
  value: {
    pageId: number
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
  context: json.value.context,
  city: json.value.city,
  language: json.value.language,
  question: json.value.questions[0].question,
  answerLines: json.value.questions[0].answerLines,
  poor: false,
})

export default mapToQuestion
