import { FormGroup } from '@mui/material'
import React, { ReactElement } from 'react'

import AnswerLine from './AnswerLine'

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
        : [...annotationAnswerLines, index].sort()
    )

  return (
    <FormGroup>
      {lines.map((line, index) => (
        <AnswerLine
          // eslint-disable-next-line react/no-array-index-key
          key={index}
          text={line}
          isSelected={annotationAnswerLines.includes(index)}
          changed={annotationAnswerLines.includes(index) !== answerLines.includes(index)}
          onToggle={() => onToggle(index)}
          disabled={disabled}
        />
      ))}
    </FormGroup>
  )
}

export default AnswerLines
