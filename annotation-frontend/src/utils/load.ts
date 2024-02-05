const load = async <T>(url: string, json: boolean, body?: string): Promise<T> => {
  const headers = body ? { headers: { 'Content-Type': 'application/json' } } : {}

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

  if (json) {
    return response.json()
  }
  // @ts-expect-error ignore
  return undefined
}

export default load
