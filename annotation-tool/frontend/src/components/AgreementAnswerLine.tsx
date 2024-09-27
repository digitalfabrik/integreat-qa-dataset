import { Checkbox as MaterialCheckbox, FormControlLabel } from '@mui/material'
import React, { ReactElement } from 'react'
import styled from 'styled-components'

const Container = styled.div`
  display: flex;
`

const StyledFormControlLabel = styled(FormControlLabel)<{ $agreement: boolean; $isSelected: boolean }>`
  ${props => props.$isSelected && (props.$agreement ? 'color: green !important;' : 'color: red !important;')}
`

const StyledCheckbox = styled(MaterialCheckbox)<{ $agreement: boolean; checked: boolean; overrideColor?: string }>`
  ${props =>
    props.checked &&
    (props.$agreement
      ? `color: ${props.overrideColor ?? 'green'} !important;`
      : `color: ${props.overrideColor ?? 'red'} !important;`)}
  align-self: start;
  padding: 0;
`

type AgreementAnswerLineProps = {
  text: string
  isSelected0: boolean
  isSelected1: boolean
  isAdjacent0?: boolean
  isAdjacent1?: boolean
}

const AgreementAnswerLine = ({
  text,
  isSelected0,
  isSelected1,
  isAdjacent0 = false,
  isAdjacent1 = false,
}: AgreementAnswerLineProps): ReactElement => (
  <Container>
    <StyledFormControlLabel
      $isSelected={isSelected0}
      $agreement={isSelected0 === isSelected1}
      label=''
      control={
        <StyledCheckbox
          checked={isSelected0 || isAdjacent0}
          $agreement={(isSelected0 || isAdjacent0) === isSelected1}
          overrideColor={isAdjacent0 ? 'blue' : undefined}
        />
      }
    />
    <StyledFormControlLabel
      $isSelected={isSelected1}
      $agreement={isSelected0 === isSelected1}
      label={text}
      control={
        <StyledCheckbox
          checked={isSelected1 || isAdjacent1}
          $agreement={isSelected0 === (isSelected1 || isAdjacent1)}
          overrideColor={isAdjacent1 ? 'blue' : undefined}
        />
      }
    />
  </Container>
)

export default AgreementAnswerLine
