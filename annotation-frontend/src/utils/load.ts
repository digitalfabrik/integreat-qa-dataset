const load = async <S, T>(url: string, map: (json: S) => T, body?: string): Promise<T> => {
  const headers = typeof body === 'string' ? { headers: { 'Content-Type': 'application/json' } } : {}

  const requestOptions = body
    ? {
        method: 'POST',
        body,
        ...headers,
      }
    : {
        method: 'GET',
      }

  const response = await fetch(url, requestOptions)

  const NOT_FOUND = 404
  if (response.status === NOT_FOUND) {
    throw new Error('notFound')
  }
  if (!response.ok) {
    throw new Error('unknownError')
  }

  const json = await response.json()
  return map(json)
}

export default load
