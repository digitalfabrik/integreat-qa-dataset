import { FormGroup } from '@mui/material'
import React, { ReactElement } from 'react'
import styled from 'styled-components'

import AnswerLine from './AnswerLine'

const Divider = styled.div`
  height: 1px;
  border-bottom: 1px solid grey;
`

type AnswerLinesProps = {
  context: string
  answerLines: number[]
  annotationAnswerLines: number[]
  onChange: (answerLines: number[]) => void
  disabled: boolean
}

const AnswerLines = ({ context, answerLines, annotationAnswerLines, onChange, disabled }: AnswerLinesProps): ReactElement => {
  const lines = context.split('\n')
  const onToggle = (index: number) =>
    onChange(
      annotationAnswerLines.includes(index)
        ? annotationAnswerLines.filter(it => it !== index)
        : [...annotationAnswerLines, index].sort(),
    )

  return (
    <FormGroup>
      {lines.map((line, index) => (
        <span key={line}>
          <AnswerLine
            text={line}
            isSelected={annotationAnswerLines.includes(index)}
            changed={annotationAnswerLines.includes(index) !== answerLines.includes(index)}
            onToggle={() => onToggle(index)}
            disabled={disabled}
          />
          <Divider />
        </span>
      ))}
    </FormGroup>
  )
}

export default AnswerLines
