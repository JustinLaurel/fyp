yInterceptA = -74.06494835
currentTempCoefA = -0.572109952
dieselFlowCoefA = 13264.89424
biomassMassCoefA = -135.3764743
charMassCoefA = -160.6001534

yInterceptB = -73.11675143
currentTempCoefB = -0.567786812
dieselFlowCoefB = 13027.81686
biomassMassCoefB = -131.3458291
charMassCoefB = -155.1985973

def yAcalc(currentTemp, dieselFlow, biomassMass, charMass, nitrogenFlow):
  return currentTempCoefA*0 + dieselFlowCoefA*dieselFlow + biomassMassCoefA*biomassMass + charMassCoefA*0 + yInterceptA

def yBcalc(currentTemp, dieselFlow, biomassMass, charMass, nitrogenFlow):
  return currentTempCoefB*0 + dieselFlowCoefB*dieselFlow + biomassMassCoefB*biomassMass + charMassCoefB*0 + yInterceptA

def calcUc(datasetA, datasetB):
  CURRENT_TEMP = 2
  DIESEL_FLOW = 3
  NITROGEN_FLOW = 1
  BIOMASS_MASS = 4
  CHAR_MASS = 5
  term1 = 0
  term2 = 0

  for datumA in datasetA:
    yAB = yBcalc(
      datumA[CURRENT_TEMP],
      datumA[DIESEL_FLOW],
      datumA[BIOMASS_MASS],
      datumA[CHAR_MASS],
      datumA[NITROGEN_FLOW]
    )
    yAA = yAcalc(
      datumA[CURRENT_TEMP],
      datumA[DIESEL_FLOW],
      datumA[BIOMASS_MASS],
      datumA[CHAR_MASS],
      datumA[NITROGEN_FLOW]
    )
    term1 += ((yAB - yAA) ** 2)

  for datumB in datasetB:
    yBA = yAcalc(
      datumB[CURRENT_TEMP],
      datumB[DIESEL_FLOW],
      datumB[BIOMASS_MASS],
      datumB[CHAR_MASS],
      datumB[NITROGEN_FLOW]
    )
    yBB = yBcalc(
      datumB[CURRENT_TEMP],
      datumB[DIESEL_FLOW],
      datumB[BIOMASS_MASS],
      datumB[CHAR_MASS],
      datumB[NITROGEN_FLOW]
    )
    term2 += ((yBA - yBB) ** 2)

  uc = (term1 + term2)**(1/2)
  
  return uc
