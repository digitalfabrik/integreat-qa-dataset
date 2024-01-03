import { FormControl, InputLabel, MenuItem, Select } from '@mui/material'
import React, { ReactElement } from 'react'
import { useTranslation } from 'react-i18next'

type DropdownSettingProps = {
  key: string
  title: string
  value: string
  options: string[]
  onChange: (value: string) => void
}

const DropdownSetting = ({ key, title, value, options, onChange }: DropdownSettingProps): ReactElement => {
  const { t } = useTranslation()
  return (
    <FormControl fullWidth>
      <InputLabel id={`${key}-label`}>{t(title)}</InputLabel>
      <Select
        id={key}
        labelId={`${key}-label`}
        value={value}
        label={t(title)}
        onChange={event => onChange(event.target.value)}>
        {options.map(it => (
          <MenuItem key={it} value={it}>
            {t(it)}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  )
}

export default DropdownSetting
