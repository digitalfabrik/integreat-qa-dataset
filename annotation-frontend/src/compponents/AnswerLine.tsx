import { Checkbox } from '@mui/material'
import React, { ReactElement } from 'react'
import styled from 'styled-components'

import StyledFormControlLabel from './StyledFormControlLabel'

const Container = styled.div`
  vertical-align: center;
  margin: 4px 0;
`

const StyledCheckbox = styled(Checkbox)`
  align-self: start;
  padding: 0;
`

type AnswerLineProps = {
  text: string
  isSelected: boolean
  onToggle: () => void
}

const AnswerLine = ({ text, isSelected, onToggle }: AnswerLineProps): ReactElement => (
  <Container>
    <StyledFormControlLabel control={<StyledCheckbox checked={isSelected} onChange={onToggle} />} label={text} />
  </Container>
)

export default AnswerLine
