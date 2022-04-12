import math

yInterceptA = 18.01231884
x1CoefA = 0
x2CoefA = -1.700724638
x3CoefA = 0
x4CoefA = 0

yInterceptB = 16.68
x1CoefB = 0
x2CoefB = -1.433333333
x3CoefB = 0
x4CoefB = 0

def yAcalc(x1, x2, x3, x4):
  return x3CoefA*x3 + yInterceptA
  # return x1CoefA*x1 + x2CoefA*x2 + x3CoefA*x3 + x4CoefA*x4 + yInterceptA

def yBcalc(x1, x2, x3, x4):
  return x3CoefA*x3 + yInterceptB
  # return x1CoefA*x1 + x2CoefA*x2 + x3CoefA*x3 + x4CoefB*x4 + yInterceptB

def calcUc(datasetA, datasetB):
  X_1 = 0
  X_2 = 1
  X_3 = 2
  X_4 = 3
  term1 = 0
  term2 = 0

  for datumA in datasetA:
    if math.isnan((datumA[X_1])): break
    yAB = yBcalc(
      datumA[X_1],
      datumA[X_2],
      datumA[X_3],
      datumA[X_4],
    )
    yAA = yAcalc(
      datumA[X_1],
      datumA[X_2],
      datumA[X_3],
      datumA[X_4],
    )
    term1 += ((yAB - yAA) ** 2)

  for datumB in datasetB:
    if math.isnan((datumB[X_1])): break
    yBA = yAcalc(
      datumB[X_1],
      datumB[X_2],
      datumB[X_3],
      datumB[X_4],
    )
    yBB = yBcalc(
      datumB[X_1],
      datumB[X_2],
      datumB[X_3],
      datumB[X_4],
    )
    term2 += ((yBA - yBB) ** 2)

  uc = (term1 + term2)**(1/2)
  
  return uc
