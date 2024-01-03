import { useCallback, useState } from 'react'

import load from '../utils/load'
import mapToQuestion, { Question } from '../utils/mapToQuestion'

type Annotation = {
  answerLines: number[]
  poor: boolean
}

type QuestionStatus =
  | {
      status: 'loading'
      question: null
      annotation: null
      error: null
    }
  | {
      status: 'error'
      question: null
      annotation: null
      error: string
    }
  | {
      status: 'ready' | 'edited' | 'submitting' | 'submitted'
      question: Question
      annotation: Annotation
      error: string | null
    }

const initialQuestion: QuestionStatus = { status: 'loading', question: null, annotation: null, error: null }

type Return = {
  currentQuestion: QuestionStatus
  showPrevious: (() => void) | null
  showNext: () => void
  editAnnotation: (question: Question, annotation: Annotation) => void
  submitAnnotation: () => void
}

const useLoadQuestion = (
  user: string,
  city: string | null,
  language: string | null,
  evidence: string | null,
): Return => {
  const [questions, setQuestions] = useState<QuestionStatus[]>([initialQuestion])
  const [currentIndex, setCurrentIndex] = useState(0)
  const currentQuestion = questions[currentIndex]

  const updateQuestion = useCallback(
    (newQuestion: QuestionStatus, index: number = currentIndex) => {
      const newQuestions = questions.map((it, loopIndex) => (loopIndex === index ? newQuestion : it))
      setQuestions(newQuestions)
    },
    [questions, currentIndex],
  )

  const loadNextQuestion = useCallback(
    (index: number) => {
      // TODO Adjust url, sanitize
      const url = new URL(`https://api.annotations.tuerantuer.org/question/${user}`)
      if (city !== null) {
        url.searchParams.append('city', city)
      }
      if (language !== null) {
        url.searchParams.append('language', language)
      }
      if (evidence !== null) {
        url.searchParams.append('evidence', (evidence === 'withEvidence').toString())
      }

      load(url.toString(), mapToQuestion)
        .then(question =>
          updateQuestion(
            {
              status: 'ready',
              question,
              annotation: { answerLines: question.answerLines, poor: false },
              error: null,
            },
            index,
          ),
        )
        .catch(error =>
          updateQuestion(
            {
              status: 'error',
              error: error.message,
              question: null,
              annotation: null,
            },
            index,
          ),
        )
    },
    [updateQuestion, user, city, language, evidence],
  )

  const showPrevious = useCallback(() => setCurrentIndex(currentIndex > 0 ? currentIndex - 1 : 0), [currentIndex])
  const showNext = useCallback(() => {
    const newIndex = currentIndex + 1
    setCurrentIndex(newIndex)

    if (newIndex === questions.length) {
      setQuestions([...questions, initialQuestion])
      loadNextQuestion(newIndex)
    }
  }, [loadNextQuestion, questions, currentIndex])

  const editAnnotation = useCallback(
    (question: Question, annotation: Annotation) => {
      updateQuestion({
        status:
          question.answerLines === annotation.answerLines && question.poor === annotation.poor ? 'ready' : 'edited',
        question,
        annotation,
        error: null,
      })
    },
    [updateQuestion],
  )
  const submitAnnotation = useCallback(() => {
    if (currentQuestion.status === 'edited') {
      updateQuestion({
        ...currentQuestion,
        status: 'submitting',
      })
      // TODO Submit
      const url = 'https://api.annotations.tuerantuer.org/annotation'
      load(url, () => undefined, JSON.stringify(currentQuestion.annotation))
        .then(() =>
          updateQuestion({
            ...currentQuestion,
            status: 'submitted',
            question: {
              ...currentQuestion.question,
              answerLines: currentQuestion.annotation.answerLines,
              poor: currentQuestion.annotation.poor,
            },
          }),
        )
        .catch(error =>
          updateQuestion({
            ...currentQuestion,
            status: 'edited',
            error: error.message,
          }),
        )
    }
  }, [updateQuestion, currentQuestion])

  return {
    currentQuestion,
    showNext,
    showPrevious: currentIndex > 1 ? showPrevious : null,
    editAnnotation,
    submitAnnotation,
  }
}

export default useLoadQuestion
