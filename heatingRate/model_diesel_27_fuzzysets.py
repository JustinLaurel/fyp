from tkinter import CURRENT
import numpy
import pandas as pandas
from helpers import *

currentTempFuzzySets = VariableFuzzySets([
  FuzzySet(None, 293, 323),
  FuzzySet(293, 323, 353),
  FuzzySet(323, 353, 383),
  FuzzySet(353, 383, 413),
  FuzzySet(383, 413, 443),
  FuzzySet(413, 443, 473),
  FuzzySet(443, 473, 503),
  FuzzySet(473, 503, 533),
  FuzzySet(503, 533, 563),
  FuzzySet(533, 563, 593),
  FuzzySet(563, 593, 623),
  FuzzySet(593, 623, 653),
  FuzzySet(623, 653, 683),
  FuzzySet(653, 683, 713),
  FuzzySet(683, 713, 743),
  FuzzySet(713, 743, 773),
  FuzzySet(743, 773, 803),
  FuzzySet(773, 803, 833),
  FuzzySet(803, 833, 863),
  FuzzySet(833, 863, 893),
  FuzzySet(863, 893, 923),
  FuzzySet(893, 923, 953),
  FuzzySet(923, 953, 983),
  FuzzySet(953, 983, 1013),
  FuzzySet(983, 1013, 1043),
  FuzzySet(1013, 1043, 1073),
  FuzzySet(1043, 1073, None),
])

HEATING_RATE = 0
CURRENT_TEMP = 1
DIESEL_FLOW = 2
NITROGEN_FLOW = 3
BIOMASS_MASS = 4
CHAR_MASS = 5

def generateFuzzyRules():
  fuzzyRules = []
  for setsVariable1 in currentTempFuzzySets.sets:
    fuzzyRules.append(FuzzyRule([setsVariable1]))

  return fuzzyRules

def evaluate(dataRow, fuzzyRules, consequentParamsList): # fuzzyRules and consequentParamsList must be the same length
  INTERCEPT = 0
  CURRENT_TEMP = 2

  totalOutput = 0
  totalFiringStrength = 0

  index = 0
  for rule in fuzzyRules:
    consequentParams = consequentParamsList[index]
    intercept = consequentParams[INTERCEPT]
    currentTempCoef = consequentParams[1]
    currentTemp = dataRow[CURRENT_TEMP]

    ruleFiringStrength = rule.calcFiringStrength([currentTemp])
    ruleOut = ruleFiringStrength * (
      intercept + currentTempCoef*currentTemp
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