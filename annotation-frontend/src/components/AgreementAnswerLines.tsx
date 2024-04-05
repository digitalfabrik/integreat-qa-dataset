import { FormGroup } from '@mui/material'
import React, { ReactElement } from 'react'

import AgreementAnswerLine from './AgreementAnswerLine'

type AgreementAnswerLinesProps = {
  context: string
  answerLines: number[][]
  adjacent: number[][]
}

const AgreementAnswerLines = ({ context, answerLines, adjacent }: AgreementAnswerLinesProps): ReactElement => {
  const lines = context.split('\n')

  return (
    <FormGroup>
      {lines.map(
        (line, index) =>
          // Don't show title
          index !== 0 && (
            <AgreementAnswerLine
              // eslint-disable-next-line react/no-array-index-key
              key={index}
              text={line}
              isSelected0={answerLines[0].includes(index)}
              isSelected1={answerLines[1].includes(index)}
              isAdjacent0={adjacent[0].includes(index)}
              isAdjacent1={adjacent[1].includes(index)}
            />
          ),
      )}
    </FormGroup>
  )
}

export default AgreementAnswerLines
