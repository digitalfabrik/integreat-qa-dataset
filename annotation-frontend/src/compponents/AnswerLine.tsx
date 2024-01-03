import { Checkbox, FormControlLabel } from '@mui/material'
import React, { ReactElement } from 'react'

type AnswerLineProps = {
  text: string
  isSelected: boolean
  onToggle: () => void
}

const AnswerLine = ({ text, isSelected, onToggle }: AnswerLineProps): ReactElement => (
  <div>
    <FormControlLabel control={<Checkbox checked={isSelected} onChange={onToggle} />} label={text} />
  </div>
)

export default AnswerLine
