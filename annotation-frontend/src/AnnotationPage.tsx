import { Button, CircularProgress } from '@mui/material'
import React, { ReactElement } from 'react'
import { useTranslation } from 'react-i18next'
import styled from 'styled-components'

import AnswerLines from './compponents/AnswerLines'
import DropdownSetting from './compponents/DropdownSetting'
import useLoadQuestion from './hooks/useLoadQuestion'
import useLoadQuestionSelections from './hooks/useLoadQuestionSelections'
import useSetting from './hooks/useSetting'

const Container = styled.div`
  display: flex;
  flex-direction: column;
  gap: 32px;
  padding: 32px;
`

const LoadingSpinnerContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
`

const Title = styled.h1`
  margin: 0;
`

const ButtonContainer = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: end;
  gap: 32px;
`

const AnnotationPage = (): ReactElement => {
  const { value: user } = useSetting<string>('user')
  const { value: city, update: setCity } = useSetting<string>('city')
  const { value: language, update: setLanguage } = useSetting<string>('language')
  const { t } = useTranslation()

  const questionSelections = useLoadQuestionSelections(user ?? 'asdf', t)

  const { currentQuestion, showPrevious, showNext, editAnnotation, submitAnnotation, isPrevious } = useLoadQuestion(
    user ?? 'asdf',
    city,
    language,
  )

  // if (currentQuestion.status === 'loading') {
  if (true) {
    return (
      <LoadingSpinnerContainer>
        <CircularProgress />
      </LoadingSpinnerContainer>
    )
  }

  if (currentQuestion.status === 'error') {
    return <div>currentQuestion.error</div>
  }

  const { context, answerLines, question } = currentQuestion.question
  const { answerLines: editedAnswerLines, poor: editedPoor } = currentQuestion.annotation

  const edited = answerLines === editedAnswerLines

  return (
    <Container>
      <DropdownSetting
        title={t('questionSelection')}
        value={
          questionSelections.find(it => it.city === city && it.language === language) ??
          // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
          questionSelections.find(it => it.city === null && it.language === null)!
        }
        options={questionSelections}
        onChange={({ city, language }) => {
          setCity(city)
          setLanguage(language)
        }}
      />
      <Title>{question}</Title>
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

      <ButtonContainer>
        {showPrevious && (
          <Button variant='text' onClick={showPrevious}>
            {t('previous')}
          </Button>
        )}
        <Button variant='contained' onClick={submitAnnotation} disabled={!edited}>
          {t('submit')}
        </Button>
        <Button variant='text' onClick={showNext}>
          {t(isPrevious ? 'showNext' : 'skip')}
        </Button>
      </ButtonContainer>
    </Container>
  )
}

export default AnnotationPage
