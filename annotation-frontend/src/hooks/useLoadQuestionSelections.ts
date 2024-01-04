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

const useLoadQuestionSelections = (user: string, t: TFunction): QuestionSelectionWithLabel[] => {
  const request = useCallback(() => {
    const url = new URL(`${BASE_URL}/question-selections`)
    url.searchParams.append('user', user)
    return load(url.toString(), (response: QuestionSelection[]) => response)
  }, [user])

  const randomLabel: QuestionSelectionWithLabel = { city: null, language: null, count: null, label: t('random') }
  const data = useLoadAsync(request).data ?? []
  const dataWithLabel = data.map(it => ({ ...it, label: `${it.city} - ${t(it.language)} (${it.count})` }))
  const languageLabels = [...new Set(data.map(it => it.language))].map(it => ({
    city: null,
    language: it,
    count: null,
    label: t(it),
  }))

  return [randomLabel, ...languageLabels, ...dataWithLabel]
}

export default useLoadQuestionSelections
