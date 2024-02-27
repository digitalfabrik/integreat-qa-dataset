import { FormControl, InputLabel, MenuItem, Select } from '@mui/material'
import React, { ReactElement } from 'react'
import styled from 'styled-components'

const StyledFormControl = styled(FormControl)`
  width: 300px;
`

type DropdownSettingProps = {
  value: string
  options: string[]
  onChange: (value: string) => void
}

const DropdownSetting = ({ value, options, onChange }: DropdownSettingProps): ReactElement => (
  <StyledFormControl>
    <InputLabel id='agreement-selection-label'>Agreement</InputLabel>
    <Select
      id='agreement-selection'
      labelId='agreement-selection-label'
      value={value}
      label={value}
      onChange={event => onChange(event.target.value)}>
      {options.map(it => (
        <MenuItem key={it} value={it}>
          {it}
        </MenuItem>
      ))}
    </Select>
  </StyledFormControl>
)

export default DropdownSetting
