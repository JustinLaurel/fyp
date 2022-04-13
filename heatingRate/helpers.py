def splitData(data):
  datasetA = []
  datasetB = []

  alternatingIndex = 2
  for datum in data:
    if alternatingIndex % 2 == 0:
      datasetA.append(datum)
    else:
      datasetB.append(datum)
    alternatingIndex += 1

  return [datasetA, datasetB]

def addHeatingRateHeaders(excelSheet):
  excelSheet.write(0, 0, 'Heating Rate (K/s)')
  excelSheet.write(0, 1, 'Current T (K)')
  excelSheet.write(0, 2, 'Diesel Flowrate (kg/s)')
  excelSheet.write(0, 3, 'Nitrogen Flowrate (kg/s)')
  excelSheet.write(0, 4, 'Biomass mass (kg)')
  excelSheet.write(0, 5, 'Char mass (kg)')
  return excelSheet

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

class VariableFuzzySets:
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

class FuzzyRule:
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
