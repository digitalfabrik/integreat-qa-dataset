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
  questions: (Question & { adjacent0: number[]; adjacent1: number[] })[]
}

const isAdjacent = (line: number, answers: number[], others: number[]): boolean =>
  !others.includes(line) &&
  ((answers.includes(line - 1) && others.includes(line - 1)) ||
    (answers.includes(line + 1) && others.includes(line + 1)))

const addAdjacent = (answers0: number[], answers1: number[], recursion: number, previous: number[] = []): number[] => {
  const adjacent = Array.from(new Set(answers1.filter(it => isAdjacent(it, answers1, answers0))))
  return recursion > 1
    ? addAdjacent([...answers0, ...adjacent], answers1, recursion - 1, [...adjacent, ...previous])
    : [...adjacent, ...previous]
}

const useLoadRows = ({ agreement }: Props): Return => {
  const request = useCallback(() => load<RowJson[]>(`${BASE_URL}/rows`, true), [])

  const { refresh, ...response } = useLoadAsync(request)
  const data = response.data ?? []

  // add_adjacent = lambda answers0, answers1: list(set(set(answers0).union([line for line in answers1 if adjacent(line, answers1, answers0)])))

  return {
    questions: mapRowsToQuestions(data)
      .filter(it => it.annotations.length === 2)
      .filter(it => agreement === 'random' || compareAnnotations(it.annotations[0], it.annotations[1]) === agreement)
      .map(it => ({
        ...it,
        adjacent0: addAdjacent(it.annotations[0].answerLines, it.annotations[1].answerLines, 3),
        adjacent1: addAdjacent(it.annotations[1].answerLines, it.annotations[0].answerLines, 3),
      })),
  }
}

export default useLoadRows
