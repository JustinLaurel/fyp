from tkinter import CURRENT
import numpy
import pandas as pandas
from helpers import *

dieselFlowFuzzySets = VariableFuzzySets([
  FuzzySet(None, 0.0015, 0.014875),
  FuzzySet(0.0015, 0.014875, 0.02825),
  FuzzySet(0.014875, 0.02825, 0.041625),
  FuzzySet(0.02825, 0.041625, 0.055),
  FuzzySet(0.041625, 0.055, None)
])
currentTempFuzzySets = VariableFuzzySets([
  FuzzySet(None, 293, 488),
  FuzzySet(293, 488, 683),
  FuzzySet(488, 683, 878),
  FuzzySet(683, 878, 1073),
  FuzzySet(878, 1073, None)
])
HEATING_RATE = 0
CURRENT_TEMP = 1
DIESEL_FLOW = 2
NITROGEN_FLOW = 3
BIOMASS_MASS = 4
CHAR_MASS = 5

def generateFuzzyRules():
  file = pandas.ExcelFile(r'C:\Users\Spring\Desktop\heatingRateModel\main_reduced_size.xlsx')
  data = pandas.read_excel(file, 'main').values

  def calcRuleDegree(degree1, degree2): return degree1*degree2

  fuzzyRules = []
  for dieselSet in dieselFlowFuzzySets.sets:
    for tempSet in currentTempFuzzySets.sets:
      fuzzyRules.append(FuzzyRule([tempSet, dieselSet]))

  return fuzzyRules

def evaluate(dataRow, fuzzyRules, consequentParamsList): # fuzzyRules and consequentParamsList must be the same length
  DIESEL_FLOW = 2
  CURRENT_TEMP = 1
  INTERCEPT = 0

  totalOutput = 0
  totalFiringStrength = 0

  index = 0
  for rule in fuzzyRules:
    consequentParams = consequentParamsList[index]
    intercept = consequentParams[INTERCEPT]
    currentTempCoef = consequentParams[2]
    dieselFlowCoef = consequentParams[1]

    currentTemp = dataRow[CURRENT_TEMP]
    dieselFlow = dataRow[DIESEL_FLOW]

    ruleFiringStrength = rule.calcFiringStrength([currentTemp, dieselFlow])
    ruleOut = ruleFiringStrength * (
      intercept + currentTempCoef*currentTemp + dieselFlowCoef *dieselFlow
    )
    totalOutput += ruleOut
    totalFiringStrength += ruleFiringStrength
    if (totalFiringStrength < 0): raise RuntimeError('firing strength is negative')
    index += 1
  index = 0

  output = totalOutput / totalFiringStrength
  return output
