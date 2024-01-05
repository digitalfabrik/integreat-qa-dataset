import { FormControl, InputLabel, MenuItem, Select } from '@mui/material'
import React, { ReactElement } from 'react'
import { useTranslation } from 'react-i18next'

import { QuestionSelectionWithLabel } from '../hooks/useLoadQuestionSelections'

type DropdownSettingProps = {
  value: QuestionSelectionWithLabel
  options: QuestionSelectionWithLabel[]
  onChange: (value: QuestionSelectionWithLabel) => void
}

const QuestionSelectionSetting = ({ value, options, onChange }: DropdownSettingProps): ReactElement => {
  const { t } = useTranslation()
  return (
    <FormControl>
      <InputLabel id='question-selection-label'>{t('questionSelection')}</InputLabel>
      <Select
        id='question-selection'
        labelId='question-selection-label'
        value={value.label}
        label={value.label}
        // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
        onChange={event => onChange(options.find(it => it.label === event.target.value)!)}>
        {options.map(it => (
          <MenuItem key={it.label} value={it.label}>
            {it.label}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  )
}

export default QuestionSelectionSetting
