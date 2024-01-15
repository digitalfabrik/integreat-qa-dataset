import { Alert, Button, CircularProgress, TextField } from '@mui/material'
import React, { ReactElement } from 'react'
import { useTranslation } from 'react-i18next'
import styled from 'styled-components'

import AnswerLines from './components/AnswerLines'
import Checkbox from './components/Checkbox'
import QuestionSelectionSetting from './components/QuestionSelectionSetting'
import useLoadQuestion from './hooks/useLoadQuestion'
import useLoadQuestionSelections from './hooks/useLoadQuestionSelections'
import useSetting from './hooks/useSetting'
import { equals } from './utils/equals'

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

const Question = styled.h1`
  margin: 0;
`

const Title = styled.h3`
  margin: 0;
`

const HighlightBox = styled.div`
  display: flex;
  flex-direction: column;
  gap: 16px;
  background-color: #fafafa;
  border-radius: 4px;
  padding: 20px;
  box-shadow:
    0 1px 3px rgb(0 0 0 / 10%),
    0 1px 2px rgb(0 0 0 / 15%);
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

type AnnotationPageProps = {
  user: string
}

const AnnotationPage = ({ user }: AnnotationPageProps): ReactElement => {
  const { value: city, update: setCity } = useSetting<string>('city')
  const { value: language, update: setLanguage } = useSetting<string>('language')
  const { t } = useTranslation()

  const { questionSelections, refresh: refreshQuestionSelections } = useLoadQuestionSelections(user, t)

  const { currentQuestion, showPrevious, showNext, editAnnotation, submitAnnotation, isPrevious } = useLoadQuestion(
    user,
    city,
    language,
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

  const { context, answerLines, question, noAnswer, comment } = currentQuestion.question
  const {
    answerLines: annotatedAnswerLines,
    noAnswer: annotatedNoAnswer,
    comment: annotatedComment,
  } = currentQuestion.annotation

  const unchanged =
    equals(annotatedAnswerLines, answerLines) && noAnswer === annotatedNoAnswer && comment === annotatedComment
  const title = context.slice(0, context.indexOf('\n'))

  return (
    <Container>
      <QuestionSelectionSettingContainer>{RenderedQuestionSelectionSetting}</QuestionSelectionSettingContainer>

      <Question>{question}</Question>
      <div>{t('instructions')}</div>

      <HighlightBox>
        <Title>{title}</Title>
        <AnswerLines
          context={context}
          answerLines={answerLines}
          annotationAnswerLines={annotatedAnswerLines}
          disabled={annotatedNoAnswer}
          onChange={newAnswerLines =>
            editAnnotation(currentQuestion, {
              answerLines: newAnswerLines,
              noAnswer: annotatedNoAnswer,
              comment: annotatedComment,
            })
          }
        />
      </HighlightBox>

      <CheckboxContainer>
        <Checkbox
          isSelected={annotatedNoAnswer}
          changed={annotatedNoAnswer !== noAnswer}
          text={t('noAnswer')}
          onToggle={() =>
            editAnnotation(currentQuestion, {
              answerLines: annotatedAnswerLines,
              noAnswer: !annotatedNoAnswer,
              comment: annotatedComment,
            })
          }
        />
      </CheckboxContainer>

      <TextField
        variant='outlined'
        label={t('comment')}
        value={annotatedComment}
        onChange={event =>
          editAnnotation(currentQuestion, {
            answerLines: annotatedAnswerLines,
            noAnswer: annotatedNoAnswer,
            comment: event.target.value,
          })
        }
      />

      {currentQuestion.status === 'submitted' && unchanged && <Alert severity='success'>{t('submitted')}</Alert>}

      <ButtonContainer>
        {showPrevious && (
          <Button variant='text' onClick={showPrevious}>
            {t('previous')}
          </Button>
        )}
        <Button
          variant='contained'
          disabled={unchanged}
          onClick={() => {
            submitAnnotation().then(refreshQuestionSelections)
          }}>
          {t('submit')}
        </Button>
        <Button variant='text' onClick={showNext}>
          {t(isPrevious ? 'next' : 'skip')}
        </Button>
      </ButtonContainer>
    </Container>
  )
}

export default AnnotationPage
