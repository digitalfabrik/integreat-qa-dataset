import { Button, CircularProgress } from '@mui/material'
import React, { ReactElement } from 'react'
import { useTranslation } from 'react-i18next'

import AnswerLines from './compponents/AnswerLines'
import DropdownSetting from './compponents/DropdownSetting'
import useLoadCities from './hooks/useLoadCities'
import useLoadLanguages from './hooks/useLoadLanguages'
import useLoadQuestion from './hooks/useLoadQuestion'
import useSetting from './hooks/useSetting'
import { fromLabel, RANDOM_LABEL, toLabel } from './utils/settingsLabels'

const AnnotationPage = (): ReactElement => {
  const { value: user, update: setUser } = useSetting<string>('user')
  const { value: city, update: setCity } = useSetting<string>('city')
  const { value: language, update: setLanguage } = useSetting<string>('language')
  const { value: evidence, update: setEvidence } = useSetting<string>('evidence')
  const { t } = useTranslation()

  const cities = useLoadCities()
  const languages = useLoadLanguages()
  const evidences = ['random', 'withEvidence', 'withoutEvidence']

  const { currentQuestion, showPrevious, showNext, editAnnotation, submitAnnotation } = useLoadQuestion(
    user ?? '',
    city,
    language,
    evidence,
  )

  if (currentQuestion.status === 'loading') {
    return <CircularProgress />
  }

  if (currentQuestion.status === 'error') {
    return <div>currentQuestion.error</div>
  }

  const { context, answerLines, question, poor } = currentQuestion.question
  const { answerLines: editedAnswerLines, poor: editedPoor } = currentQuestion.annotation

  const edited = answerLines === editedAnswerLines

  return (
    <div>
      <div>
        <DropdownSetting
          key='city-setting'
          title={t('city')}
          value={toLabel(city)}
          options={[RANDOM_LABEL, ...cities]}
          onChange={label => setCity(fromLabel(label))}
        />
        <DropdownSetting
          key='language-setting'
          title={t('language')}
          value={toLabel(language)}
          options={[RANDOM_LABEL, ...languages]}
          onChange={label => setLanguage(fromLabel(label))}
        />
        <DropdownSetting
          key='evidence-setting'
          title={t('questionType')}
          value={toLabel(evidence)}
          options={[RANDOM_LABEL, ...evidences]}
          onChange={label => setEvidence(fromLabel(label))}
        />
      </div>
      {question}
      <AnswerLines
        context={context}
        answerLines={editedAnswerLines}
        onChange={newAnswerLines =>
          editAnnotation(currentQuestion.question, {
            answerLines: newAnswerLines,
            poor: editedPoor,
          })
        }
      />
      {showPrevious && (
        <Button variant='text' onClick={showPrevious}>
          {t('showPrevious')}
        </Button>
      )}
      <Button variant='contained' onClick={submitAnnotation} disabled={!edited}>
        {t('submit')}
      </Button>
      <Button variant='text' onClick={showNext}>
        {t('showNext')}
      </Button>
    </div>
  )
}

export default AnnotationPage
