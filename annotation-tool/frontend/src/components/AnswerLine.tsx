import React, { ReactElement } from 'react'
import styled from 'styled-components'

import Checkbox from './Checkbox'

const StyledCheckbox = styled(Checkbox)`
  width: 100%;
`

type AnswerLineProps = {
  text: string
  isSelected: boolean
  changed: boolean
  onToggle: () => void
  disabled: boolean
}

const AnswerLine = ({ text, isSelected, changed, onToggle, disabled }: AnswerLineProps): ReactElement => (
  <div>
    <StyledCheckbox onToggle={onToggle} isSelected={isSelected} disabled={disabled} text={text} changed={changed} />
  </div>
)

export default AnswerLine
