yInterceptA = 356.9462623
currentTempCoefA = -0.572109952
dieselFlowCoefA = 13264.89424
nitrogenFlowCoefA = -20.40010245
biomassMassCoefA = -135.3764743
charMassCoefA = -160.6001534

yInterceptB = 359.3426031
currentTempCoefB = -0.567786812
dieselFlowCoefB = 13027.81686
nitrogenFlowCoefB = -21.40536397
biomassMassCoefB = -131.3458291
charMassCoefB = -155.1985973

def yAcalc(currentTemp, dieselFlow, nitrogenFlow, biomassMass, charMass):
  return currentTempCoefA*currentTemp + dieselFlowCoefA*dieselFlow + nitrogenFlowCoefA*nitrogenFlow + biomassMassCoefA*biomassMass + charMassCoefA*charMass + yInterceptA

def yBcalc(currentTemp, dieselFlow, nitrogenFlow, biomassMass, charMass):
  return currentTempCoefB*currentTemp + dieselFlowCoefB*dieselFlow + nitrogenFlowCoefB*nitrogenFlow + biomassMassCoefB*biomassMass + charMassCoefB*charMass + yInterceptB

def calcUc(datasetA, datasetB):
  CURRENT_TEMP = 1
  DIESEL_FLOW = 2
  NITROGEN_FLOW = 3
  BIOMASS_MASS = 4
  CHAR_MASS = 5
  term1 = 0
  term2 = 0

  for datumA in datasetA:
    yAB = yBcalc(
      datumA[CURRENT_TEMP],
      datumA[DIESEL_FLOW],
      datumA[NITROGEN_FLOW],
      datumA[BIOMASS_MASS],
      datumA[CHAR_MASS]
    )
    yAA = yAcalc(
      datumA[CURRENT_TEMP],
      datumA[DIESEL_FLOW],
      datumA[NITROGEN_FLOW],
      datumA[BIOMASS_MASS],
      datumA[CHAR_MASS]
    )
    term1 += ((yAB - yAA) ** 2)

  for datumB in datasetB:
    yBA = yAcalc(
      datumB[CURRENT_TEMP],
      datumB[DIESEL_FLOW],
      datumB[NITROGEN_FLOW],
      datumB[BIOMASS_MASS],
      datumB[CHAR_MASS]
    )
    yBB = yBcalc(
      datumB[CURRENT_TEMP],
      datumB[DIESEL_FLOW],
      datumB[NITROGEN_FLOW],
      datumB[BIOMASS_MASS],
      datumB[CHAR_MASS]
    )
    term2 += ((yBA - yBB) ** 2)

  uc = (term1 + term2)**(1/2)
  
  return uc
