import { useCallback } from 'react'

import { BASE_URL } from '../constants/url'
import load from '../utils/load'
import useLoadAsync from './useLoadAsync'

const useLoadCities = (): string[] => {
  const request = useCallback(() => load(`${BASE_URL}/cities`, (it: string[]) => it), [])
  return useLoadAsync(request).data ?? []
}

export default useLoadCities
