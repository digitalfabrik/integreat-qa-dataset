export const equals = <T>(array1: T[], array2: T[]): boolean =>
  array1.length === array2.length && array1.every((it, index) => it === array2[index])
