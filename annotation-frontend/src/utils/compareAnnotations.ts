import { equals } from './equals'
import { Annotation } from './mapToQuestion'

export type AgreementType = 'random' | 'agreement' | 'one-sided' | 'overlap' | 'none'

const compareAnnotations = (annotation0: Annotation, annotation1: Annotation): AgreementType => {
  const answers0 = annotation0.answerLines
  const answers1 = annotation1.answerLines
  const intersection = answers0.filter(it => answers1.includes(it))

  if (equals(answers0, answers1)) {
    return 'agreement'
  } else if (intersection.length > 0 && (equals(answers0, intersection) || equals(answers1, intersection))) {
    return 'one-sided'
  } else if (intersection.length > 0) {
    return 'overlap'
  }
  return 'none'
}

export default compareAnnotations
