from .classes import *

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


def generateFuzzyPremises():
  fuzzyPremises = []

  # Modifications start here
  for biomassMassSet in biomassMassFuzzySets:
    fuzzyPremises.append(FuzzyPremise([biomassMassSet]))
  # Modifications end here

  return fuzzyPremises

# Modify input fuzzy sets here
biomassMassFuzzySets = generateFuzzySets(
  [25, 60],
  7
)
#Modifications end here
