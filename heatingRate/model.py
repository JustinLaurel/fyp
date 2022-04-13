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
  # for datum in data:
  #   highestDiesel = dieselFlowFuzzySets.getHighestMembership(datum[DIESEL_FLOW])
  #   highestTemp = currentTempFuzzySets.getHighestMembership(datum[CURRENT_TEMP])
  #   degree = highestDiesel.membership * highestTemp.membership
