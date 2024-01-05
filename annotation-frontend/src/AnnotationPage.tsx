import { Button, CircularProgress } from '@mui/material'
import React, { ReactElement } from 'react'
import { useTranslation } from 'react-i18next'
import styled from 'styled-components'

import AnswerLines from './components/AnswerLines'
import QuestionSelectionSetting from './components/QuestionSelectionSetting'
import useLoadQuestion from './hooks/useLoadQuestion'
import useLoadQuestionSelections from './hooks/useLoadQuestionSelections'
import useSetting from './hooks/useSetting'
import { equals } from './utils/equals'
import Checkbox from './components/Checkbox'

const Container = styled.div`
    display: flex;
    flex-direction: column;
    gap: 32px;
    padding: 32px;
`

const Centered = styled.div`
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 32px;
`

const QuestionSelectionSettingContainer = styled.div`
    display: flex;
    justify-content: end;
`

const Title = styled.h1`
    margin: 0;
`

const CheckboxContainer = styled.div`
    display: flex;
    flex-direction: row;
    gap: 32px;
`

const ButtonContainer = styled.div`
    display: flex;
    flex-direction: row;
    justify-content: end;
    gap: 32px;
`

// const PoorQuestionButton = styled(Button)<{ $changed: boolean }>`
//     color: ${props => props.$changed ? CHANGED_COLOR : DANGER_COLOR} !important;
//     border-color: ${props => props.$changed ? CHANGED_COLOR : DANGER_COLOR} !important;
// `

type AnnotationPageProps = {
  user: string
}

const AnnotationPage = ({ user }: AnnotationPageProps): ReactElement => {
  const { value: city, update: setCity } = useSetting<string>('city')
  const { value: language, update: setLanguage } = useSetting<string>('language')
  const { t } = useTranslation()

  const questionSelections = useLoadQuestionSelections(user, t)

  const { currentQuestion, showPrevious, showNext, editAnnotation, submitAnnotation, isPrevious } = useLoadQuestion(
    user,
    city,
    language
  )

  if (currentQuestion.status === 'loading') {
    return (
      <Centered>
        <CircularProgress />
      </Centered>
    )
  }

  const RenderedQuestionSelectionSetting = (
    <QuestionSelectionSetting
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
  )

  if (currentQuestion.status === 'error') {
    return (
      <Centered>
        {currentQuestion.error === 'notFound' && RenderedQuestionSelectionSetting}
        {t(currentQuestion.error)}
      </Centered>
    )
  }

  const { context, answerLines, question, poor } = currentQuestion.question
  const { answerLines: annotationAnswerLines, poor: annotatedPoor } = currentQuestion.annotation

  const unchanged = equals(annotationAnswerLines, answerLines) && poor === annotatedPoor

  return (
    <Container>
      <QuestionSelectionSettingContainer>{RenderedQuestionSelectionSetting}</QuestionSelectionSettingContainer>

      <Title>{question}</Title>
      <AnswerLines
        context={context}
        answerLines={answerLines}
        annotationAnswerLines={annotationAnswerLines}
        disabled={annotatedPoor}
        onChange={newAnswerLines =>
          editAnnotation(currentQuestion.question, {
            answerLines: newAnswerLines,
            poor: annotatedPoor
          })
        }
      />

      <CheckboxContainer>
        <Checkbox
          isSelected={annotationAnswerLines.length === 0}
          changed={annotationAnswerLines.length !== answerLines.length}
          text={t('noAnswer')}
          disabled={annotatedPoor}
          onToggle={() =>
            editAnnotation(currentQuestion.question, {
              answerLines: annotationAnswerLines.length === 0 ? answerLines : [],
              poor: annotatedPoor
            })
          }
        />
        <Checkbox
          isSelected={annotatedPoor}
          changed={annotatedPoor !== poor}
          text={t('poorQuestion')}
          isDanger
          onToggle={() =>
            editAnnotation(currentQuestion.question, {
              answerLines: annotationAnswerLines,
              poor: !annotatedPoor
            })}
        />
      </CheckboxContainer>

      <ButtonContainer>
        {showPrevious && (
          <Button variant="text" onClick={showPrevious}>
            {t('previous')}
          </Button>
        )}
        <Button variant="contained" onClick={submitAnnotation}>
          {t(unchanged ? 'approve' : 'submit')}
        </Button>
        <Button variant="text" onClick={showNext}>
          {t(isPrevious ? 'showNext' : 'skip')}
        </Button>
      </ButtonContainer>
    </Container>
  )
}

export default AnnotationPage
