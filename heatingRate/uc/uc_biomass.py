yInterceptA = 390.2063501
biomassCoefA = -135.3764743

yInterceptB = 382.8568387
biomassCoefB = -131.3458291

def yAcalc(biomassMass):
  return biomassCoefA*biomassMass + yInterceptA

def yBcalc(biomassMass):
  return biomassCoefB*biomassMass + yInterceptB

def calcUc(datasetA, datasetB):
  BIOMASS_MASS = 4
  term1 = 0
  term2 = 0

  for datumA in datasetA:
    yAB = yBcalc(
      datumA[BIOMASS_MASS],
    )
    yAA = yAcalc(
      datumA[BIOMASS_MASS],
    )
    term1 += ((yAB - yAA) ** 2)

  for datumB in datasetB:
    yBA = yAcalc(
      datumB[BIOMASS_MASS],
    )
    yBB = yBcalc(
      datumB[BIOMASS_MASS],
    )
    term2 += ((yBA - yBB) ** 2)

  uc = (term1 + term2)**(1/2)
  
  return uc
