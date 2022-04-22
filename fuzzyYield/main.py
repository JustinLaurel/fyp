import numpy
import pandas as pandas
from .model import generateFuzzyPremises
from .classes import *
import xlsxwriter
import os

fuzzyPremises = generateFuzzyPremises()

# # Modify file path to location of your data's excel file
# dirname = os.path.dirname(__file__)
# filename = os.path.join(dirname, '.\model_data.xlsx')
# file = pandas.ExcelFile(filename)
# data = pandas.read_excel(file, 'main').values

# Modify indexing constants for your inputs and output in excel file
BIOMASS_MASS = 3

TUNGSTEN_HEATING_RATE = 2 # Controller output
# Modify indexing constants end here

def calcXRow(datum, fuzzyPremises):
  # Modify to access all input variables you want in your fuzzy model here
  biomassMass = datum[BIOMASS_MASS]
  inputValues = [
    datum[BIOMASS_MASS]
  ]
  # Modify input variable access ends here

  firingStrengths = getFiringStrengths(
    fuzzyPremises,
    inputValues
  )
  totalFiringStrength = 0
  for strength in firingStrengths:
    totalFiringStrength += strength

  if (totalFiringStrength == 0): 
    raise Exception('Some datapoints are outside of fuzzy MF ranges. Sanitize the data first')
  
  betaValues = []
  for strength in firingStrengths:
    betaValues.append(strength / totalFiringStrength)

  # Modify: one additional for-loop across betaValues for each variable in your fuzzy model
  X_row = []
  for beta in betaValues:
    X_row.append(beta)
  for beta in betaValues:
    X_row.append(beta * biomassMass)
  # Modify end

  return X_row
  

def getFiringStrengths(fuzzyPremises, inputValues):
  firingStrengths = []

  for rule in fuzzyPremises:
    firingStrengths.append(
      rule.calcFiringStrength([*inputValues])
    )

  return firingStrengths

def generateP(X, Y):
  X = numpy.array(X)
  
  X_transpose = X.T
  Y = numpy.array(Y)
  dotProduct = numpy.dot(X_transpose, X)

  P = None
  try:
    P = numpy.linalg.inv(dotProduct)
  except:
    P = numpy.linalg.pinv(dotProduct)
  P = numpy.dot(P, X_transpose)
  P = numpy.dot(P, Y)

  return P

def identifyFuzzyController(data):
  X = []
  Y = []
  for datum in data:
    X.append(
      calcXRow(datum, fuzzyPremises)
    )
    Y.append([
      datum[TUNGSTEN_HEATING_RATE]
    ])
  P = generateP(X, Y)
  print('p array length=' + str(len(P)))

  index = 0
  consequentParamsList = []

  # Modify: range interval to access P is the total number of possible permutations of all premise membership functions
  # eg: You have 3 input variables, one with 3 MFs and two with 5 MFs. Then the interval is 3*5*5=75
  intercepts = P[:7]
  biomassMass = P[7:14]
  # Modify ends here

  for param in intercepts:
    consequentParamsList.append(
      [
        intercepts[index][0],
        biomassMass[index][0],
        # NEW_INPUT_VARIABLE[index][0],
      ]
    )
    index += 1
  # Modification end

  controller = FuzzyController(fuzzyPremises, consequentParamsList)
  return controller

# # Evaluate output using input data with fuzzy model
# book = xlsxwriter.Workbook('model_data_fuzzyOutput.xlsx')
# sheet1 = book.add_worksheet('main')

# sheet1.write(0, 0, 'Inferred tar yield')
# sheet1.write(0, 1, 'Tungsten temperature')
# sheet1.write(0, 2, 'Biomass mass')

# controller = FuzzyController(fuzzyPremises, consequentParamsList)
# for index in range(len(data)):
#   rowToWrite = index + 1
#   datum = data[index]

#   inferredOutput = controller.evaluate([
#     datum[TUNGSTEN_TEMP],
#     datum[BIOMASS_MASS]
#   ])

#   sheet1.write(rowToWrite, 0, inferredOutput)
#   sheet1.write(rowToWrite, 1, datum[TUNGSTEN_TEMP])
#   sheet1.write(rowToWrite, 2, datum[BIOMASS_MASS])
# book.close()
