from tkinter import CURRENT
import numpy
import pandas as pandas
from dieselFuzzySets import evaluationCreator
from dieselFuzzySets import evaluate
from dieselFuzzySets import generateFuzzyRules
from helpers import *
import xlsxwriter
from uc.uc_heatingRate import calcUc

fuzzyRules = generateFuzzyRules()

file = pandas.ExcelFile(r'C:\Users\Spring\Desktop\heatingRateModel\diesel_flow.xlsx')
data = pandas.read_excel(file, 'main').values
datasetA = pandas.read_excel(file, 'datasetA').values
datasetB = pandas.read_excel(file, 'datasetB').values
data = numpy.delete(data, 0, 0)
datasetA = numpy.delete(datasetA, 0, 0)
datasetB = numpy.delete(datasetB, 0, 0)

DIESEL_FLOW = 0
HEATING_RATE = 1
CURRENT_TEMP = 2
NITROGEN_FLOWRATE = 3
SOLID_MASS = 4

def calcXRow(datum, fuzzyRules):
  values = [
    datum[HEATING_RATE],
    datum[CURRENT_TEMP],
    datum[SOLID_MASS],
  ]
  firingStrengths = getFiringStrengths(fuzzyRules, values)
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
    X_row.append(beta * values[0])
  for beta in betaValues:
    X_row.append(beta * values[1])
  for beta in betaValues:
    X_row.append(beta * values[2])

  return X_row
  

def getFiringStrengths(fuzzyRules, values):
  firingStrengths = []

  for rule in fuzzyRules:
    firingStrengths.append(
      rule.calcFiringStrength(values)
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

def calculateConsequentParameters(data, fuzzyRules, OUTPUT_INDEX = 0):
  X = []
  Y = []
  for datum in data:
    X.append(
      calcXRow(datum, fuzzyRules)
    )
      
    Y.append([
      datum[OUTPUT_INDEX]
    ])
  P = generateP(X, Y)

  consequentParamsList = formatPMatrix(P, fuzzyRules)
  return consequentParamsList

consequentParamsList = calculateConsequentParameters(data, fuzzyRules, DIESEL_FLOW)
consequentParamsListDataA = calculateConsequentParameters(datasetA, fuzzyRules, DIESEL_FLOW)
consequentParamsListDataB = calculateConsequentParameters(datasetB, fuzzyRules, DIESEL_FLOW)


# Calculate UC
print('uc=' + str(
  calcUc(
    datasetA,
    datasetB,
    evaluationCreator(fuzzyRules, consequentParamsListDataA),
    evaluationCreator(fuzzyRules, consequentParamsListDataB)  
  )
))

# Evaluate output using input data with fuzzy model
book = xlsxwriter.Workbook('fuzzyOutput.xlsx')
sheet1 = book.add_worksheet('main')
sheet1.write(0, 0, 'Inferred Diesel Flowrate')
sheet1.write(0, 1, 'Diesel Flow Rate')
sheet1.write(0, 2, 'Heating Rate')
sheet1.write(0, 3, 'Current Temperature')
sheet1.write(0, 4, 'Nitrogen Flow Rate')
sheet1.write(0, 5, 'Solid Mass')
rowIndex = 1
for row in data:
  inferredOutput = evaluate(row, fuzzyRules, consequentParamsList)
  sheet1.write(rowIndex, 0, inferredOutput)
  sheet1.write(rowIndex, 1, row[DIESEL_FLOW])
  sheet1.write(rowIndex, 2, row[HEATING_RATE])
  sheet1.write(rowIndex, 3, row[CURRENT_TEMP])
  sheet1.write(rowIndex, 4, row[NITROGEN_FLOWRATE])
  sheet1.write(rowIndex, 5, row[SOLID_MASS])
  rowIndex += 1
book.close()
