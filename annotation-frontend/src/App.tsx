import i18next from 'i18next'
import React, { ReactElement, useEffect, useState } from 'react'
import { initReactI18next } from 'react-i18next'

import AgreementPage from './AgreementPage'
import AnnotationPage from './AnnotationPage'
import LandingPage from './LandingPage'
import useSetting from './hooks/useSetting'
import translations from './translations'

i18next.use(initReactI18next).init({
  lng: navigator.language,
  debug: true,
  resources: translations,
  fallbackLng: 'en',
})

const App = (): ReactElement => {
  const { value: landingPageShown, update } = useSetting<boolean>('LANDING_PAGE_SHOWN')
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

  if (window.location.pathname === '/agreement') {
    return <AgreementPage user={user} />
  }

  return landingPageShown ? (
    <AnnotationPage user={user} />
  ) : (
    <LandingPage user={user} setLandingPageShown={() => update(true)} />
  )
}

export default App
