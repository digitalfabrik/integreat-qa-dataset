import i18next from 'i18next'
import React, { ReactElement } from 'react'
import { initReactI18next } from 'react-i18next'

import AnnotationPage from './AnnotationPage'
import translations from './translations'

i18next.use(initReactI18next).init({
  lng: navigator.language,
  debug: true,
  resources: translations,
  fallbackLng: 'en',
})

const App = (): ReactElement => (
  <div className='App'>
    <AnnotationPage />
  </div>
)

export default App
