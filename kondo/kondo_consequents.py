import numpy
import pandas as pandas
from helpers import splitData

file = pandas.ExcelFile(r'C:\Users\Spring\Desktop\heatingRateModel\kondo.xlsx')
data = pandas.read_excel(file, 'main').values
print(data)

X1_INDEX = 0
X2_INDEX = 1
X3_INDEX = 2
X4_INDEX = 3
OUTPUT_INDEX = 4

def calcXRow(datum):
  x1 = datum[X1_INDEX]
  x2 = datum[X2_INDEX]
  x3 = datum[X3_INDEX]
  x4 = datum[X4_INDEX]

  degrees = calcDegreeOfMemberships(x3)
  totalDegree = 0
  for degree in degrees:
    totalDegree += degree

  betas = []
  for degree in degrees:
    betas.append(degree / totalDegree)

  X_row = []
  for beta in betas:
    X_row.append(beta)
  for beta in betas:
    X_row.append(beta * x1)
  for beta in betas:
    X_row.append(beta * x2)
  for beta in betas:
    X_row.append(beta * x3)
  for beta in betas:
    X_row.append(beta * x4)

  return X_row
  

def calcDegreeOfMemberships(x):
  memberships = [0, 0]
  RULE_1 = 0
  RULE_2 = 1

  if (x < 2.5): memberships[RULE_1] = 1
  elif (x > 3.5): memberships[RULE_1] = 0
  else:
    memberships[RULE_1] = (-x + 3.5)

  if (x > 3.5): memberships[RULE_2] = 1
  elif (x < 2.5): memberships[RULE_2] = 0
  else:
    memberships[RULE_2] = (x - 2.5)

  return memberships

def generateP(X, Y):
  X = numpy.array(X)
  X_transpose = X.T
  Y = numpy.array(Y)

  P = numpy.linalg.inv(
    numpy.dot(X_transpose, X)
  )
  P = numpy.dot(P, X_transpose)
  P = numpy.dot(P, Y)

  return P



X = []
Y = []
for datum in data:
  X.append(
    calcXRow(datum)
  )
  Y.append([
    datum[OUTPUT_INDEX]
  ])

print(generateP(X, Y))
