import { Checkbox as MaterialCheckbox, FormControlLabel } from '@mui/material'
import React, { ReactElement } from 'react'
import styled from 'styled-components'

const Container = styled.div`
  display: flex;
`

const StyledFormControlLabel = styled(FormControlLabel)<{ $agreement: boolean; $isSelected: boolean }>`
  ${props => props.$isSelected && (props.$agreement ? 'color: green !important;' : 'color: red !important;')}
`

const StyledCheckbox = styled(MaterialCheckbox)<{ $agreement: boolean; checked: boolean }>`
  ${props => props.checked && (props.$agreement ? 'color: green !important;' : 'color: red !important;')}
  align-self: start;
  padding: 0;
`

type AgreementAnswerLineProps = {
  text: string
  isSelected0: boolean
  isSelected1: boolean
}

const AgreementAnswerLine = ({ text, isSelected0, isSelected1 }: AgreementAnswerLineProps): ReactElement => (
  <Container>
    <StyledFormControlLabel
      $isSelected={isSelected0}
      $agreement={isSelected0 === isSelected1}
      label=''
      control={<StyledCheckbox checked={isSelected0} $agreement={isSelected0 === isSelected1} />}
    />
    <StyledFormControlLabel
      $isSelected={isSelected1}
      $agreement={isSelected0 === isSelected1}
      label={text}
      control={<StyledCheckbox checked={isSelected1} $agreement={isSelected0 === isSelected1} />}
    />
  </Container>
)

export default AgreementAnswerLine
