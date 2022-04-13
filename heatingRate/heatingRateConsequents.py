import numpy
import pandas as pandas
from helpers import *
from model import generateFuzzyRules

fuzzyRules = generateFuzzyRules()

file = pandas.ExcelFile(r'C:\Users\Spring\Desktop\heatingRateModel\main_reduced_size.xlsx')
data = pandas.read_excel(file, 'main').values
print(data)

DIESEL_FLOW = 2
CURRENT_TEMP = 1
HEATING_RATE = 0

def calcXRow(datum, fuzzyRules):
  dieselFlow = datum[DIESEL_FLOW]
  currentTemp = datum[CURRENT_TEMP]

  firingStrengths = getFiringStrengths(fuzzyRules, currentTemp, dieselFlow)
  totalFiringStrength = 0
  for strength in firingStrengths:
    totalFiringStrength += strength

  betaValues = []
  for strength in firingStrengths:
    betaValues.append(strength / totalFiringStrength)

  X_row = []
  for beta in betaValues:
    X_row.append(beta)
  for beta in betaValues:
    X_row.append(beta * dieselFlow)
  for beta in betaValues:
    X_row.append(beta * currentTemp)

  return X_row
  

def getFiringStrengths(fuzzyRules, currentTemp, dieselFlow):
  firingStrengths = []

  for rule in fuzzyRules:
    firingStrengths.append(
      rule.calcFiringStrength([currentTemp, dieselFlow])
    )

  return firingStrengths

def generateP(X, Y):
  X = numpy.array(X)
  X_transpose = X.T
  Y = numpy.array(Y)
  dotProduct = numpy.dot(X_transpose, X)
  P = numpy.linalg.inv(
    dotProduct
  )
  P = numpy.dot(P, X_transpose)
  P = numpy.dot(P, Y)

  return P


dieselFlowFuzzySets = [
  FuzzySet(None, 0.0015, 0.014875),
  FuzzySet(0.0015, 0.014875, 0.02825),
  FuzzySet(0.014875, 0.02825, 0.041625),
  FuzzySet(0.02825, 0.041625, 0.055),
  FuzzySet(0.041625, 0.055, None)
]
currentTempFuzzySets = [
  FuzzySet(None, 293, 488),
  FuzzySet(293, 488, 683),
  FuzzySet(488, 683, 878),
  FuzzySet(683, 878, 1073),
  FuzzySet(878, 1073, None)
]

X = []
Y = []
for datum in data:
  X.append(
    calcXRow(datum, fuzzyRules)
  )
  Y.append([
    datum[HEATING_RATE]
  ])
P = generateP(X, Y)
print(generateP(X, Y))
print('p array length=' + str(len(P)))

index = 0
consequentParams = []
intercepts = P[:25]
dieselFlow = P[25:50]
currentTemp = P[50:75]

for param in intercepts:
  consequentParams.append(
    [intercepts[index][0], dieselFlow[index][0], currentTemp[index][0]]
  )
  index += 1

# consequentParams.append([intercept, currentTemp, dieselFlow])
print(str(consequentParams))
