yInterceptA = 1.905805554
heatingRateCoefA = 0
mNitrogenCoefA = -1.275120051

yInterceptB = 1.907931667
heatingRateCoefB = 0
mNitrogenCoefB = -1.277328737

def yAcalc(heatingRate, mNitrogen):
  return heatingRateCoefA*heatingRate + mNitrogenCoefA*mNitrogen + yInterceptA

def yBcalc(heatingRate, mNitrogen):
  return heatingRateCoefB*heatingRate + mNitrogenCoefB*mNitrogen + yInterceptB

def calcUc(datasetA, datasetB):
  HEATING_RATE = 0
  M_NITROGEN = 0

  term1 = 0
  term2 = 0

  for datumA in datasetA:
    yAB = yBcalc(
      datumA[HEATING_RATE],
      datumA[M_NITROGEN]
    )
    yAA = yAcalc(
      datumA[HEATING_RATE],
      datumA[M_NITROGEN]
    )
    term1 += ((yAB - yAA) ** 2)

  for datumB in datasetB:
    yBA = yAcalc(
      datumB[HEATING_RATE],
      datumB[M_NITROGEN]
    )
    yBB = yBcalc(
      datumB[HEATING_RATE],
      datumB[M_NITROGEN]
    )
    term2 += ((yBA - yBB) ** 2)

  uc = (term1 + term2)**(1/2)
  
  return uc
