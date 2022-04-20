from classes import *

def generateFuzzyPremises():
  fuzzyPremises = []

  # Modifications start here
  for tungstenSet in tungstenHeatingRateFuzzySets:
    for biomassSet in biomassMassFuzzySets:
      fuzzyPremises.append(FuzzyPremise([tungstenSet, biomassSet]))
  # Modifications end here

  return fuzzyPremises

def generateFuzzySets(variableRange, numberOfMfs):
  if (numberOfMfs < 2): raise Exception('Minimum 3 membership functions are needed for each fuzzy set')
  if ((numberOfMfs % 2) == 0): raise Exception('Number of membership functions must be odd')

  lowerRange = variableRange[0]
  upperRange = variableRange[1]

  interval = (upperRange - lowerRange) / (numberOfMfs - 1)

  fuzzySets = []
  currentMiddleX = lowerRange
  for index in range(numberOfMfs):
    if (index == 0): 
      fuzzySets.append(FuzzySet(None, lowerRange, lowerRange + interval))
      currentMiddleX += interval
    elif (index < (numberOfMfs - 1)): 
      fuzzySets.append(FuzzySet(currentMiddleX - interval, currentMiddleX, currentMiddleX + interval))
      currentMiddleX += interval
    else: 
      fuzzySets.append(FuzzySet(currentMiddleX - interval, currentMiddleX, None))
      break

  return fuzzySets


# Modifications start here
tungstenHeatingRateFuzzySets = generateFuzzySets(
  [700, 2000],
  5
)
biomassMassFuzzySets = generateFuzzySets(
  [25, 60],
  5
)
#Modifications end here
