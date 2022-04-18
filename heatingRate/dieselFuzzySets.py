from tkinter import CURRENT
import numpy
import pandas as pandas
from helpers import *

# heatingRateFuzzySets = VariableFuzzySets([
#   FuzzySet(None, 100, 137.5),
#   FuzzySet(100, 137.5, 175),
#   FuzzySet(137.5, 175, 212.5),
#   FuzzySet(175, 212.5, 250),
#   FuzzySet(212.5, 250, None)
# ])
# currentTempFuzzySets = VariableFuzzySets([
#   FuzzySet(None, 293, 488),
#   FuzzySet(293, 488, 683),
#   FuzzySet(488, 683, 878),
#   FuzzySet(683, 878, 1073),
#   FuzzySet(878, 1073, None)
# ])
# solidMassFuzzySets = VariableFuzzySets([
#   FuzzySet(None, 0, 0.375),
#   FuzzySet(0, 0.375, 0.75),
#   FuzzySet(0.375, 0.75, 1.125),
#   FuzzySet(0.75, 1.125, 1.5),
#   FuzzySet(1.125, 1.5, None)
# ])
# nitrogenFlowFuzzySets = VariableFuzzySets([
#   FuzzySet(None, 0.6, 0.75),
#   FuzzySet(0.6, 0.75, 0.90),
#   FuzzySet(0.75, 0.90, 1.05),
#   FuzzySet(0.90, 1.05, 1.2),
#   FuzzySet(1.05, 1.2, None)
# ])


heatingRateFuzzySets = VariableFuzzySets([
  FuzzySet(None, 100, 175),
  FuzzySet(100, 175, 250),
  FuzzySet(175, 250, None)
])
currentTempFuzzySets = VariableFuzzySets([
  FuzzySet(None, 293, 683),
  FuzzySet(293, 683, 1073),
  FuzzySet(683, 1073, None)
])
solidMassFuzzySets = VariableFuzzySets([
  FuzzySet(None, 0, 0.75),
  FuzzySet(0, 0.75, 1.5),
  FuzzySet(0.75, 1.5, None),
])


HEATING_RATE = 0
CURRENT_TEMP = 1
DIESEL_FLOW = 2
NITROGEN_FLOW = 3
BIOMASS_MASS = 4
CHAR_MASS = 5

def generateFuzzyRules():
  fuzzyRules = []
  for setsVariable1 in heatingRateFuzzySets.sets:
    for setsVariable2 in currentTempFuzzySets.sets:
      for setsVariable3 in solidMassFuzzySets.sets:
        fuzzyRules.append(FuzzyRule([setsVariable1, setsVariable2, setsVariable3]))

  return fuzzyRules

def evaluate(dataRow, fuzzyRules, consequentParamsList): # fuzzyRules and consequentParamsList must be the same length
  INTERCEPT = 0
  HEATING_RATE = 1
  CURRENT_TEMP = 2
  NITROGEN_FLOW = 3
  SOLID_MASS = 4

  totalOutput = 0
  totalFiringStrength = 0

  index = 0
  for rule in fuzzyRules:
    consequentParams = consequentParamsList[index]
    intercept = consequentParams[INTERCEPT]
    heatingRateCoef = consequentParams[1]
    currentTempCoef = consequentParams[2]
    solidMassCoef = consequentParams[3]
    heatingRate = dataRow[HEATING_RATE]
    currentTemp = dataRow[CURRENT_TEMP]
    solidMass = dataRow[SOLID_MASS]

    ruleFiringStrength = rule.calcFiringStrength([heatingRate, currentTemp, solidMass])
    ruleOut = ruleFiringStrength * (
      intercept + heatingRateCoef*heatingRate + currentTempCoef*currentTemp + solidMassCoef*solidMass
    )
    totalOutput += ruleOut
    totalFiringStrength += ruleFiringStrength
    if (totalFiringStrength < 0): raise RuntimeError('firing strength is negative')
    index += 1
  index = 0

  output = totalOutput / totalFiringStrength
  return output

def evaluationCreator(fuzzyRules, consequentParamsList):
  def evaluateHolder(dataRow):
    return evaluate(dataRow, fuzzyRules, consequentParamsList)
  return evaluateHolder

def modelEvaluate(data, fuzzyRules, consequentParamsList): # fuzzyRules and consequentParamsList must be the same length
  INTERCEPT = 0

  SETPOINT_TEMP = 0
  SENSOR_TEMP = 1
  SOLID_MASS = 2
  
  totalOutput = 0
  totalFiringStrength = 0

  index = 0
  for rule in fuzzyRules:
    consequentParams = consequentParamsList[index]
    intercept = consequentParams[INTERCEPT]
    setpointTempCoef = consequentParams[1]
    sensorTempCoef = consequentParams[2]
    solidMassCoef = consequentParams[3]

    setpointTemp = data[SETPOINT_TEMP]
    sensorTemp = data[SENSOR_TEMP]
    solidMass = data[SOLID_MASS]

    ruleFiringStrength = rule.calcFiringStrength([setpointTemp, sensorTemp, solidMass])
    ruleOut = ruleFiringStrength * (
      intercept + setpointTempCoef*setpointTemp + sensorTempCoef*sensorTemp + solidMassCoef*solidMass
    )
    totalOutput += ruleOut
    totalFiringStrength += ruleFiringStrength
    if (totalFiringStrength < 0): raise RuntimeError('firing strength is negative')
    index += 1
  index = 0

  output = totalOutput / totalFiringStrength
  return output
