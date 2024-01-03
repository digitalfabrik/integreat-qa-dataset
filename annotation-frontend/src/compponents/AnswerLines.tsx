import { FormGroup } from '@mui/material'
import React, { ReactElement } from 'react'

import AnswerLine from './AnswerLine'

type AnswerLinesProps = {
  context: string
  answerLines: number[]
  onChange: (answerLines: number[]) => void
}

const AnswerLines = ({ context, answerLines, onChange }: AnswerLinesProps): ReactElement => {
  const lines = context.split('\n')
  const onToggle = (index: number) =>
    onChange(answerLines.includes(index) ? answerLines.filter(it => it !== index) : [...answerLines, index].sort())

  return (
    <FormGroup>
      {lines.map((line, index) => (
        <AnswerLine key={line} text={line} isSelected={answerLines.includes(index)} onToggle={() => onToggle(index)} />
      ))}
    </FormGroup>
  )
}

export default AnswerLines
