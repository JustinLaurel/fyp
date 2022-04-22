import math

class FuzzySet:
  def __init__(this, leftX, middleX, rightX):
    this.leftX = leftX
    this.middleX = middleX
    this.rightX = rightX

    this.isLeftmost = leftX is None
    this.isRightmost = rightX is None
    this.isNormal = not (this.isLeftmost | this.isRightmost)

  def getGradient(this):
    gradient = (1-0) / (this.middleX -
      (this.leftX) if (this.leftX is not None) else (this.rightX)
    )
    return abs(gradient)

  def getLeftIntercept(this):
    return 1 - this.getGradient()*this.middleX
  def getRightIntercept(this):
    return 1 + this.getGradient()*this.middleX
  
  def calcMembership(this, x):
    if (not this.isRightmost):
      if (x > this.rightX):
        return 0
    if (not this.isLeftmost):
      if (x < this.leftX):
        return 0
    if (this.isRightmost) & (x > this.middleX):
      return 0
    if (this.isLeftmost) & (x < this.middleX):
      return 0

    gradient = this.getGradient()
    if (not this.isLeftmost) & (x < this.middleX):
      return gradient*x + this.getLeftIntercept()
    elif (not this.isRightmost) & (x > this.middleX):
      return -gradient*x + this.getRightIntercept()
    elif (x == this.middleX): return 1

    else: raise RuntimeError('Failure at calcMembership of FuzzySet')

class FuzzySetsOneVariable:
  def __init__(this, sets):
    this.sets = sets
  
  def getHighestMembership(this, x):
    highestMembershipSet = FuzzySetData(None, 0)
    for set in this.sets:
      membership = set.calcMembership(x)
      if (membership > highestMembershipSet.membership):
        highestMembershipSet.fuzzySet = set
        highestMembershipSet.membership = membership
      return highestMembershipSet

class FuzzySetData:
  def __init__(this, fuzzySet, membership):
    this.fuzzySet = fuzzySet
    this.membership = membership

class FuzzyPremise:
  def __init__(this, premiseFuzzySets):
    this.premiseFuzzySets = premiseFuzzySets #fuzzy sets in rule premise

  # length of data array needs to be same as length of fuzzySets array
  # data array is the relevant input-output data row
  def calcFiringStrength(this, data):
    memberships = []
    index = 0
    for set in this.premiseFuzzySets:
      memberships.append(
        set.calcMembership(data[index]),
      )
      index += 1

    minMembership = memberships[0] #Apply min() function to AND statements in fuzzy clauses
    for membership in memberships:
      if membership < minMembership: minMembership = membership

    return minMembership

PREMISE = 0
CONSEQUENT = 1
class FuzzyController:
  def __init__(this, fuzzyPremises, consequentParams):
    this.rules = []

    for index in range(len(fuzzyPremises)):
      this.rules.append([
        fuzzyPremises[index],
        consequentParams[index]
      ])

  def evaluate(this, data):
    INTERCEPT = 0
    totalOutput = 0
    totalFiringStrength = 0
    for index in range(len(this.rules)):
      premise = this.rules[index][PREMISE]
      firingStrength = premise.calcFiringStrength(data)

      consequentCoefficients = this.rules[index][CONSEQUENT]
      ruleOutput = 0
      for paramIndex in range(len(consequentCoefficients)):
        if (paramIndex == INTERCEPT): 
          ruleOutput += consequentCoefficients[paramIndex]
        else:
          ruleOutput += consequentCoefficients[paramIndex] * data[paramIndex - 1]
      
      totalOutput += ruleOutput * firingStrength
      totalFiringStrength += firingStrength

    if totalFiringStrength == 0: return 0
    output = totalOutput / totalFiringStrength
    
    if math.isnan(output): raise Exception('Too many arguments to fuzzy controller')
    return output


def formatPMatrix(P, fuzzyRules):
  consequentParamsList = []

  kSize = len(fuzzyRules[0].premiseFuzzySets)
  consequentParamsCount = kSize + 1
  betaCount = len(fuzzyRules)
  higherBetaIndex = betaCount
  lowerBetaIndex = 0
  paramsListUnordered = []
  for i in range(consequentParamsCount):
    variableParam = P[lowerBetaIndex:higherBetaIndex]
    paramsListUnordered.append(variableParam)
    lowerBetaIndex += betaCount
    higherBetaIndex += betaCount

  for index in range(len(paramsListUnordered[0])):
    paramsForOneRule = []
    for paramsForOneVariable in paramsListUnordered:
      paramsForOneRule.append(paramsForOneVariable[index][0])
    consequentParamsList.append(paramsForOneRule)

  return consequentParamsList
