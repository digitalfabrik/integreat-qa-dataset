import { useCallback, useState } from 'react'

type Return<T> = {
  value: T | null
  update: (value: T | null) => void
}

const useSetting = <T>(key: string): Return<T> => {
  const initial = window.localStorage.getItem(key)
  const [value, setValue] = useState(initial ? JSON.parse(initial) : null)

  const update = useCallback(
    (newValue: T | null) => {
      setValue(newValue)
      window.localStorage.setItem(key, JSON.stringify(newValue))
    },
    [key],
  )

  return { value, update }
}

export default useSetting
