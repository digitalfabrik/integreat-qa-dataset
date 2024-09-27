import { Checkbox as MaterialCheckbox, FormControlLabel } from '@mui/material'
import React, { ReactElement } from 'react'
import styled from 'styled-components'

import { CHANGED_COLOR, DANGER_COLOR, SELECTED_COLOR } from '../constants/colors'

const StyledFormControlLabel = styled(FormControlLabel)<{
  $changed: boolean
  $selected: boolean
  $isDanger: boolean
  $disabled: boolean
}>`
  color: ${props => !props.disabled && !props.$isDanger && props.$changed && CHANGED_COLOR} !important;
  color: ${props => !props.disabled && !props.$changed && props.$selected && SELECTED_COLOR} !important;
  color: ${props => props.$isDanger && DANGER_COLOR} !important;
  width: 100%;
  margin: 0 !important;
`

const StyledCheckbox = styled(MaterialCheckbox)<{ $changed: boolean; $isDanger: boolean; $disabled: boolean }>`
  color: ${props => !props.disabled && !props.$isDanger && props.$changed && CHANGED_COLOR} !important;
  color: ${props => props.$isDanger && DANGER_COLOR} !important;
  align-self: start;
  padding: 0;
`

type AnswerLineProps = {
  text: string
  isSelected: boolean
  changed: boolean
  onToggle: () => void
  isDanger?: boolean
  disabled?: boolean
  className?: string
}

const Checkbox = ({
  text,
  isSelected,
  changed,
  onToggle,
  isDanger = false,
  disabled = false,
  className,
}: AnswerLineProps): ReactElement => (
  <StyledFormControlLabel
    $changed={changed}
    $selected={isSelected}
    $disabled={disabled}
    $isDanger={isDanger}
    label={text}
    className={className}
    control={
      <StyledCheckbox
        checked={isSelected}
        onChange={onToggle}
        $changed={changed}
        $disabled={disabled}
        disabled={disabled}
        $isDanger={isDanger}
      />
    }
  />
)

export default Checkbox
