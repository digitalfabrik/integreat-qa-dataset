export const RANDOM_LABEL = 'random'

export const fromLabel = (label: string): string | null => (label === RANDOM_LABEL ? null : label)
export const toLabel = (value: string | null): string => (value === null ? RANDOM_LABEL : value)
