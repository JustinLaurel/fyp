yInterceptA = 310.5740154
charCoefA = -160.6001534

yInterceptB = 309.743601
charCoefB = -155.1985973

def yAcalc(charMass):
  return charCoefA*charMass + yInterceptA

def yBcalc(charMass):
  return charCoefB*charMass + yInterceptB

def calcUc(datasetA, datasetB):
  CHAR_MASS = 5
  term1 = 0
  term2 = 0

  for datumA in datasetA:
    yAB = yBcalc(
      datumA[CHAR_MASS],
    )
    yAA = yAcalc(
      datumA[CHAR_MASS],
    )
    term1 += ((yAB - yAA) ** 2)

  for datumB in datasetB:
    yBA = yAcalc(
      datumB[CHAR_MASS],
    )
    yBB = yBcalc(
      datumB[CHAR_MASS],
    )
    term2 += ((yBA - yBB) ** 2)

  uc = (term1 + term2)**(1/2)
  
  return uc
