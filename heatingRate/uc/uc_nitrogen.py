yInterceptA = 307.0340866
nitrogenFlowCoefA = -20.40010245

yInterceptB = 303.6122944
nitrogenFlowCoefB = -21.40536397

def yAcalc(nitrogenFlow):
  return nitrogenFlowCoefA*nitrogenFlow + yInterceptA

def yBcalc(nitrogenFlow):
  return nitrogenFlowCoefB*nitrogenFlow + yInterceptB

def calcUc(datasetA, datasetB):
  NITROGEN_FLOW = 3
  term1 = 0
  term2 = 0

  for datumA in datasetA:
    yAB = yBcalc(
      datumA[NITROGEN_FLOW],
    )
    yAA = yAcalc(
      datumA[NITROGEN_FLOW],
    )
    term1 += ((yAB - yAA) ** 2)

  for datumB in datasetB:
    yBA = yAcalc(
      datumB[NITROGEN_FLOW],
    )
    yBB = yBcalc(
      datumB[NITROGEN_FLOW],
    )
    term2 += ((yBA - yBB) ** 2)

  uc = (term1 + term2)**(1/2)
  
  return uc
