def calcUc(
  datasetA,
  datasetB,
  modelAEvaluate,
  modelBEvaluate
):
  HEATING_RATE = 1
  DIESEL_FLOW = 3
  NITROGEN_FLOW = 1
  BIOMASS_MASS = 4
  CHAR_MASS = 5
  term1 = 0
  term2 = 0

  for datarowA in datasetA:
    yAB = modelBEvaluate(
      datarowA
    )
    yAA = modelAEvaluate(
      datarowA
    )
    term1 += ((yAB - yAA) ** 2)

  for datarowB in datasetB:
    yBA = modelAEvaluate(
      datarowB
    )
    yBB = modelBEvaluate(
      datarowB
    )
    term2 += ((yBA - yBB) ** 2)

  uc = (term1 + term2)**(1/2)
  
  return uc
