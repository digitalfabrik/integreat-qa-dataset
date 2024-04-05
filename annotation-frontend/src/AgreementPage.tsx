import { Button, CircularProgress } from '@mui/material'
import React, { ReactElement, useEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'
import styled from 'styled-components'

import AgreementAnswerLine from './components/AgreementAnswerLine'
import AgreementAnswerLines from './components/AgreementAnswerLines'
import Container from './components/Container'
import DropdownSetting from './components/DropdownSetting'
import useLoadRows from './hooks/useLoadRows'
import { AgreementType } from './utils/compareAnnotations'

const Centered = styled.div`
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 32px;
  padding: 32px;
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

const ControlContainer = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  gap: 32px;
`

const ButtonContainer = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: end;
  gap: 32px;
`

const agreementOptions = ['random', 'agreement', 'one-sided', 'overlap', 'none']

type AnnotationPageProps = {
  user: string
}

const AgreementPage = ({}: AnnotationPageProps): ReactElement => {
  const [index, setIndex] = useState(0)
  const [agreement, setAgreement] = useState<AgreementType>('random')
  const { questions: data } = useLoadRows({ agreement })
  const questions = data.filter(it => it.adjacent0.length > 2 || it.adjacent1.length > 2)
  const currentQuestion = questions[index]
  const { t } = useTranslation()

  useEffect(() => window.scrollTo({ top: 0, behavior: 'smooth' }), [index])

  if (questions.length === 0) {
    return (
      <Centered>
        <CircularProgress />
      </Centered>
    )
  }

  console.log(agreement, questions.length)

  const { context, question, annotations, adjacent0, adjacent1 } = currentQuestion

  console.log(adjacent0, adjacent1)
  const title = context.slice(0, context.indexOf('\n'))
  const annotation0 = annotations[0]!
  const annotation1 = annotations[1]!

  return (
    <Container>
      <ControlContainer>
        {/* @ts-expect-error */}
        <DropdownSetting value={agreement} options={agreementOptions} onChange={setAgreement} />

        <ButtonContainer>
          {index > 0 && (
            <Button variant='text' onClick={() => setIndex(index - 1)}>
              {t('previous')}
            </Button>
          )}
          {index < questions.length - 1 && (
            <Button variant='text' onClick={() => setIndex(index + 1)}>
              {t('next')}
            </Button>
          )}
        </ButtonContainer>
      </ControlContainer>

      <Question>{question}</Question>

      <AgreementAnswerLine text={t('noAnswer')} isSelected0={annotation0.noAnswer} isSelected1={annotation1.noAnswer} />

      <HighlightBox>
        <Title>{title.trim().endsWith('?') ? t('title', { title }) : title}</Title>
        <AgreementAnswerLines
          context={context}
          answerLines={[annotation0.answerLines, annotation1.answerLines]}
          adjacent={[adjacent0, adjacent1]}
        />
      </HighlightBox>
    </Container>
  )
}

export default AgreementPage
