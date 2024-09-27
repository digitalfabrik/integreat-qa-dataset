import { TFunction } from 'i18next'
import { useCallback } from 'react'

import { BASE_URL } from '../constants/url'
import load from '../utils/load'
import useLoadAsync from './useLoadAsync'

type QuestionSelection = {
  city: string
  language: string
  count: number
}

export type QuestionSelectionWithLabel = {
  city: string | null
  language: string | null
  count: number | null
  label: string
}

type Return = {
  questionSelections: QuestionSelectionWithLabel[]
  refresh: () => void
}

const useLoadQuestionSelections = (user: string, t: TFunction): Return => {
  const request = useCallback(() => {
    const url = new URL(`${BASE_URL}/question-selections`)
    url.searchParams.append('user', user)
    return load<QuestionSelection[]>(url.toString(), true)
  }, [user])

  const { refresh, ...response } = useLoadAsync(request)
  const data = response.data ?? []

  const randomLabel: QuestionSelectionWithLabel = { city: null, language: null, count: null, label: t('random') }
  const languageLabels = [...new Set(data.map(it => it.language))].map(it => ({
    city: null,
    language: it,
    count: null,
    label: t(it),
  }))

  return { questionSelections: [randomLabel, ...languageLabels], refresh }
}

export default useLoadQuestionSelections
