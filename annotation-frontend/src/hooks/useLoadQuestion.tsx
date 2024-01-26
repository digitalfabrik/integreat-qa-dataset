import { useCallback, useEffect, useState } from 'react'

import { BASE_URL } from '../constants/url'
import load from '../utils/load'
import mapToQuestion, { Question, QuestionJson } from '../utils/mapToQuestion'

type Annotation = {
  answerLines: number[]
  noAnswer: boolean
  comment: string
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
      status: 'ready' | 'submitting' | 'submitted'
      question: Question
      annotation: Annotation
      error: string | null
    }

const initialQuestion: QuestionStatus = { status: 'loading', question: null, annotation: null, error: null }

type Return = {
  currentQuestion: QuestionStatus
  showPrevious: (() => void) | null
  editAnnotation: (currentQuestion: QuestionStatus, annotation: Annotation) => void
  submitAnnotation: () => Promise<void>
  skip: () => Promise<void>
  isPrevious: boolean
}

const useLoadQuestion = (
  user: string,
  city: string | null,
  language: string | null,
  evidence: string | null = null,
): Return => {
  const [questions, setQuestions] = useState<QuestionStatus[]>([initialQuestion])
  const [currentIndex, setCurrentIndex] = useState(0)
  const currentQuestion = questions[currentIndex]

  const updateQuestion = useCallback((newQuestion: QuestionStatus, index: number) => {
    setQuestions(questions => questions.map((it, loopIndex) => (loopIndex === index ? newQuestion : it)))
  }, [])

  const loadNextQuestion = useCallback(
    (currentIndex: number) => {
      const url = new URL(`${BASE_URL}/question`)
      url.searchParams.append('user', user)
      if (city !== null) {
        url.searchParams.append('city', city)
      }
      if (language !== null) {
        url.searchParams.append('language', language)
      }
      if (evidence !== null) {
        url.searchParams.append('evidence', (evidence === 'withEvidence').toString())
      }

      load<QuestionJson>(url.toString(), true)
        .then(json => {
          const question = mapToQuestion(json)
          updateQuestion(
            {
              status: 'ready',
              question,
              annotation: { answerLines: question.answerLines, noAnswer: false, comment: '' },
              error: null,
            },
            currentIndex,
          )
        })
        .catch(error =>
          updateQuestion(
            {
              status: 'error',
              error: error.message,
              question: null,
              annotation: null,
            },
            currentIndex,
          ),
        )
    },
    [user, city, language, evidence, updateQuestion],
  )

  useEffect(() => {
    setCurrentIndex(0)
    setQuestions([initialQuestion])
    loadNextQuestion(0)
  }, [loadNextQuestion])

  const showPrevious = useCallback(() => setCurrentIndex(currentIndex > 0 ? currentIndex - 1 : 0), [currentIndex])
  const showNext = useCallback(() => {
    const newIndex = currentIndex + 1

    if (newIndex === questions.length) {
      setQuestions(questions => [...questions, initialQuestion])
      loadNextQuestion(newIndex)
    }
    setCurrentIndex(newIndex)
  }, [loadNextQuestion, questions, currentIndex])

  const editAnnotation = useCallback(
    (currentQuestion: QuestionStatus, annotation: Annotation) => {
      if (currentQuestion.status === 'ready' || currentQuestion.status === 'submitted') {
        updateQuestion(
          {
            ...currentQuestion,
            annotation,
          },
          currentIndex,
        )
      }
    },
    [updateQuestion, currentIndex],
  )

  const submitAnnotation = useCallback(
    async (skipped = false) => {
      if (currentQuestion.status === 'ready' || currentQuestion.status === 'submitted') {
        updateQuestion(
          {
            ...currentQuestion,
            status: 'submitting',
          },
          currentIndex,
        )
        const url = `${BASE_URL}/annotation`
        const body = JSON.stringify({
          id: currentQuestion.question.id,
          value: { ...currentQuestion.annotation, user, poor: false, skipped },
        })
        await load(url, false, body)
          .then(() =>
            updateQuestion(
              {
                ...currentQuestion,
                status: skipped ? 'ready' : 'submitted',
                question: {
                  ...currentQuestion.question,
                  answerLines: currentQuestion.annotation.answerLines,
                  noAnswer: currentQuestion.annotation.noAnswer,
                  comment: currentQuestion.annotation.comment,
                },
              },
              currentIndex,
            ),
          )
          .then(showNext)
          .catch(error => {
            console.log(error)
            updateQuestion(
              {
                ...currentQuestion,
                error: error.message,
              },
              currentIndex,
            )
          })
      }
    },
    [updateQuestion, currentQuestion, showNext, user, currentIndex],
  )

  return {
    currentQuestion,
    showPrevious: currentIndex > 0 ? showPrevious : null,
    editAnnotation,
    submitAnnotation,
    skip: () => submitAnnotation(true),
    isPrevious: currentIndex < questions.length - 1,
  }
}

export default useLoadQuestion
