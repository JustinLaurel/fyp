yInterceptA = 679.5229887
currentTempCoefA = -0.577030582

yInterceptB = 664.6304347
currentTempCoefB = -0.55689477

def yAcalc(currentTemp):
  return currentTempCoefA*currentTemp + yInterceptA

def yBcalc(currentTemp):
  return currentTempCoefB*currentTemp + yInterceptB

def calcUc(datasetA, datasetB):
  CURRENT_TEMP = 1
  term1 = 0
  term2 = 0

  for datumA in datasetA:
    yAB = yBcalc(
      datumA[CURRENT_TEMP],
    )
    yAA = yAcalc(
      datumA[CURRENT_TEMP],
    )
    term1 += ((yAB - yAA) ** 2)

  for datumB in datasetB:
    yBA = yAcalc(
      datumB[CURRENT_TEMP],
    )
    yBB = yBcalc(
      datumB[CURRENT_TEMP],
    )
    term2 += ((yBA - yBB) ** 2)

  uc = (term1 + term2)**(1/2)
  
  return uc
