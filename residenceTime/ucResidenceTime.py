yInterceptA = 4.96640187
nitrogenFlowCoefA = -1.417362396
dieselFlowCoefA = -38.92040488

yInterceptB = 4.928211301
nitrogenFlowCoefB = -1.377461054
dieselFlowCoefB = -38.86809519

def yAcalc(residenceTime, heatingRate, dieselFlow, nitrogenFlow):
  return nitrogenFlowCoefA*nitrogenFlow + dieselFlowCoefA*dieselFlow + yInterceptA

def yBcalc(residenceTime, heatingRate, dieselFlow, nitrogenFlow):
  return nitrogenFlowCoefB*nitrogenFlow + dieselFlowCoefB*dieselFlow + yInterceptB

def calcUc(datasetA, datasetB):
  RESIDENCE_TIME = 1
  HEATING_RATE = 4
  NITROGEN_FLOW = 3
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
