import ExpandMoreIcon from '@mui/icons-material/ExpandMore'
import InfoIcon from '@mui/icons-material/InfoOutlined'
import LightbulbIcon from '@mui/icons-material/LightbulbOutlined'
import ScienceIcon from '@mui/icons-material/ScienceOutlined'
import { Accordion, AccordionDetails, AccordionSummary, Button } from '@mui/material'
import React, { ReactElement, useState } from 'react'
import { useTranslation } from 'react-i18next'
import styled from 'styled-components'

import AugsburgLogo from './assets/augsburg.jpg'
import DigitalfabrikLogo from './assets/digitalfabrik.jpg'
import DortmundLogo from './assets/dortmund.jpg'
import Checkbox from './components/Checkbox'
import Container from './components/Container'
import QuestionSelectionSetting from './components/QuestionSelectionSetting'
import useLoadQuestionSelections from './hooks/useLoadQuestionSelections'
import useSetting from './hooks/useSetting'

const ImageRow = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  gap: 32px;
`

const Image = styled.img`
  height: 48px;
`

const Title = styled.h1`
  margin: 0;
`

const Description = styled.div`
  display: flex;
  flex-direction: column;
  gap: 16px;
`

const SubDescription = styled.div`
  display: flex;
  flex-direction: column;
`

const DescriptionTitle = styled.h4`
  margin: 0;
`

const ButtonContainer = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: center;
  gap: 32px;
`

export const AccordionSummaryContent = styled.div`
  display: flex;
  gap: 8px;
`

export const AccordionTitle = styled.span`
  margin: auto;
`

export const StyledAccordionDetails = styled(AccordionDetails)`
  display: flex;
  flex-direction: column;
  gap: 16px;
`

const StyledCheckbox = styled(Checkbox)`
  color: inherit !important;
`

type LandingPageProps = {
  setLandingPageShown: () => void
  user: string
}

const LandingPage = ({ setLandingPageShown, user }: LandingPageProps): ReactElement => {
  const [consent, setConsent] = useState(false)
  const { value: city, update: setCity } = useSetting<string>('city')
  const { value: language, update: setLanguage } = useSetting<string>('language')
  const { t } = useTranslation()
  const { questionSelections } = useLoadQuestionSelections(user, t)

  return (
    <Container>
      <ImageRow>
        <Image src={DigitalfabrikLogo} />
        <Image src={DortmundLogo} />
        <Image src={AugsburgLogo} />
      </ImageRow>

      <Title>{t('landingTitle')}</Title>

      <Description>
        <div>
          <DescriptionTitle>{t('ourGoal')}</DescriptionTitle>
          <span>{t('goal')}</span>
        </div>
        <div>
          <DescriptionTitle>{t('ourIdea')}</DescriptionTitle>
          <span>{t('idea')}</span>
        </div>
        <div>
          <DescriptionTitle>{t('yourHelp')}</DescriptionTitle>
          <span>{t('help')}</span>
        </div>

        <div />

        <SubDescription>
          <span>{t('omos')}</span>
          <span>{t('cooperation')}</span>
        </SubDescription>
      </Description>

      <Accordion>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>{t('moreInformation')}</AccordionSummary>

        <StyledAccordionDetails>
          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <AccordionSummaryContent>
                <InfoIcon />
                <AccordionTitle>{t('moreInformationIntegreatTitle')}</AccordionTitle>
              </AccordionSummaryContent>
            </AccordionSummary>

            <StyledAccordionDetails>
              {t('moreInformationIntegreatContent')}

              <a href='https://integreat.app'>{t('integreatLink')}</a>
              <a href='https://integreat-app.de'>{t('integreatInformationLink')}</a>
              <a href='https://tuerantuer.de/digitalfabrik/'>Tür an Tür Digitalfabrik</a>
            </StyledAccordionDetails>
          </Accordion>

          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <AccordionSummaryContent>
                <LightbulbIcon />
                <AccordionTitle>{t('moreInformationIdeaTitle')}</AccordionTitle>
              </AccordionSummaryContent>
            </AccordionSummary>

            <StyledAccordionDetails>
              {t('moreInformationIdeaContent')}

              <a href='https://integreat-app.de/datenspenden-fuer-omos/'>{t('blogLink')}</a>
            </StyledAccordionDetails>
          </Accordion>

          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <AccordionSummaryContent>
                <ScienceIcon />
                <AccordionTitle>{t('moreInformationResearchTitle')}</AccordionTitle>
              </AccordionSummaryContent>
            </AccordionSummary>

            <StyledAccordionDetails>{t('moreInformationResearchContent')}</StyledAccordionDetails>
          </Accordion>
        </StyledAccordionDetails>
      </Accordion>

      <Description>{t('questionSelectionDescription')}</Description>
      <QuestionSelectionSetting
        value={
          questionSelections.find(it => it.city === city && it.language === language) ??
          // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
          questionSelections.find(it => it.city === null && it.language === null)!
        }
        options={questionSelections}
        onChange={({ city, language }) => {
          setCity(city)
          setLanguage(language)
        }}
      />

      <StyledCheckbox text={t('consent')} isSelected={consent} onToggle={() => setConsent(it => !it)} changed={false} />

      <ButtonContainer>
        <Button variant='contained' onClick={setLandingPageShown} disabled={!consent}>
          {t('continue')}
        </Button>
      </ButtonContainer>
    </Container>
  )
}

export default LandingPage
