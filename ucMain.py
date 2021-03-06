yInterceptA = -0.819152157
residenceTimeCoefA = 0.488247273
heatingRateCoefA = 0
nitrogenFlowCoefA = 0
dieselFlowCoefA = 6.660691227

yInterceptB = -1.245498387
residenceTimeCoefB = 0.567711382
heatingRateCoefB = 0
nitrogenFlowCoefB = 0
dieselFlowCoefB = 13.91439793

def yAcalc(residenceTime, heatingRate, dieselFlow, nitrogenFlow):
  return residenceTimeCoefA*residenceTime + dieselFlowCoefA*dieselFlow + yInterceptA

def yBcalc(residenceTime, heatingRate, dieselFlow, nitrogenFlow):
  return residenceTimeCoefB*residenceTime + dieselFlowCoefB*dieselFlow + yInterceptB

def calcUc(datasetA, datasetB):
  RESIDENCE_TIME = 1
  HEATING_RATE = 3
  NITROGEN_FLOW = 4
  DIESEL_FLOW = 2
  term1 = 0
  term2 = 0

  for datumA in datasetA:
    yAB = yBcalc(
      datumA[RESIDENCE_TIME],
      datumA[HEATING_RATE],
      datumA[DIESEL_FLOW],
      datumA[NITROGEN_FLOW]
    )
    yAA = yAcalc(
      datumA[RESIDENCE_TIME],
      datumA[HEATING_RATE],
      datumA[DIESEL_FLOW],
      datumA[NITROGEN_FLOW]
    )
    term1 += ((yAB - yAA) ** 2)

  for datumB in datasetB:
    yBA = yAcalc(
      datumB[RESIDENCE_TIME],
      datumB[HEATING_RATE],
      datumB[DIESEL_FLOW],
      datumB[NITROGEN_FLOW]
    )
    yBB = yBcalc(
      datumB[RESIDENCE_TIME],
      datumB[HEATING_RATE],
      datumB[DIESEL_FLOW],
      datumB[NITROGEN_FLOW]
    )
    term2 += ((yBA - yBB) ** 2)

  uc = (term1 + term2)**(1/2)
  
  return uc
