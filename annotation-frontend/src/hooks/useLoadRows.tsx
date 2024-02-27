import { useCallback } from 'react'

import { BASE_URL } from '../constants/url'
import compareAnnotations, { AgreementType } from '../utils/compareAnnotations'
import load from '../utils/load'
import { mapRowsToQuestions, Question, RowJson } from '../utils/mapToQuestion'
import useLoadAsync from './useLoadAsync'

type Props = {
  agreement: AgreementType
}

type Return = {
  questions: Question[]
}

const useLoadRows = ({ agreement }: Props): Return => {
  const request = useCallback(() => load<RowJson[]>(`${BASE_URL}/rows`, true), [])

  const { refresh, ...response } = useLoadAsync(request)
  const data = response.data ?? []

  return {
    questions: mapRowsToQuestions(data)
      .filter(it => it.annotations.length === 2)
      .filter(it => agreement === 'random' || compareAnnotations(it.annotations[0], it.annotations[1]) === agreement),
  }
}

export default useLoadRows
