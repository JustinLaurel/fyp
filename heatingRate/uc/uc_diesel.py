yInterceptA = -171.6261233
dieselFlowCoefA = 13027.81686

yInterceptB = -175.5973041
dieselFlowCoefB = 13264.89424

def yAcalc(dieselFlow):
  return dieselFlowCoefA*dieselFlow + yInterceptA

def yBcalc(dieselFlow):
  return dieselFlowCoefB*dieselFlow + yInterceptB

def calcUc(datasetA, datasetB):
  DIESEL_FLOW = 2
  term1 = 0
  term2 = 0

  for datumA in datasetA:
    yAB = yBcalc(
      datumA[DIESEL_FLOW],
    )
    yAA = yAcalc(
      datumA[DIESEL_FLOW],
    )
    term1 += ((yAB - yAA) ** 2)

  for datumB in datasetB:
    yBA = yAcalc(
      datumB[DIESEL_FLOW],
    )
    yBB = yBcalc(
      datumB[DIESEL_FLOW],
    )
    term2 += ((yBA - yBB) ** 2)

  uc = (term1 + term2)**(1/2)
  
  return uc
