import i18next from 'i18next'
import React, { ReactElement, useEffect, useState } from 'react'
import { initReactI18next } from 'react-i18next'

import AnnotationPage from './AnnotationPage'
import translations from './translations'

i18next.use(initReactI18next).init({
  lng: navigator.language,
  debug: true,
  resources: translations,
  fallbackLng: 'en',
})

const App = (): ReactElement => {
  const [user, setUser] = useState<string>()

  useEffect(() => {
    const userUuid = window.localStorage.getItem('user')

    if (!userUuid) {
      const generatedUserUuid = window.self.crypto.randomUUID()
      window.localStorage.setItem('user', generatedUserUuid)
      setUser(generatedUserUuid)
    } else {
      setUser(userUuid)
    }
  }, [])

  if (!user) {
    return <div />
  }

  return <AnnotationPage user={user} />
}

export default App
