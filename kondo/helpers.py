import math
ZERO_MEMBERSHIP_TERM = 2  # Index of x value where degree of membership starts being zero
ONE_MEMBERSHIP_TERM = 1   # Index of x value where degree of membership starts being one
TERMINATE_TERM = 0        # Index where function terminates


def splitData(data):
  datasetA = []
  datasetB = []

  alternatingIndex = 2
  for datum in data:
    if (datum[0] == None) | math.isnan(datum[0]): break
    if alternatingIndex % 2 == 0:
      datasetA.append(datum)
    else:
      datasetB.append(datum)
    alternatingIndex += 1

  return [datasetA, datasetB]

def getClosestPointOnFunction(initialPoint, funcData):
  x = initialPoint[0]
  y = initialPoint[1]
  gradient = funcData[0]
  intercept = funcData[1]

  x_coord = (
    x + gradient*intercept - gradient*y
  ) / (1 + gradient**2)
  y_coord = gradient*x_coord + intercept

  return [x_coord, y_coord]

def calcDistanceBetweenPoints(point1, point2):
  X_COORD = 0
  Y_COORD = 1
  return math.sqrt(
    (point1[X_COORD] - point2[X_COORD]) ** 2 + \
    (point1[Y_COORD] - point2[Y_COORD]) ** 2
  )

def calcGradientIntercept(point1, point2):
  x1 = point1[0]
  y1 = point1[1]

  x2 = point2[0]
  y2 = point2[1]

  gradient = (y2-y1) / x2-x1
  intercept = y1 - gradient*x1

  return [gradient, intercept]

def calcGradientInterceptFromFuzzySet(fuzzySet):
  x1 = fuzzySet[ONE_MEMBERSHIP_TERM]
  y1 = 1

  x2 = fuzzySet[ZERO_MEMBERSHIP_TERM]
  y2 = 0

  return calcGradientIntercept([x1, y1], [x2, y2])

def reverseValues(variable1, variable2):
  placeholder = variable1
  variable1 = variable2
  variable2 = placeholder
  return [variable1, variable2]

def calcNewOneMembershipTerm(fuzzySet, x, wTilde):
  point1 = [
    fuzzySet[ZERO_MEMBERSHIP_TERM],
    0
  ]
  point2 = [
    x,
    wTilde
  ]

  [gradient, intercept] = calcGradientIntercept(point1, point2)
  newOneMembershipTerm = (1-intercept) / gradient

  return newOneMembershipTerm

def calcNewZeroMembershipTerm(fuzzySet, x, w0):
  point1 = [
    fuzzySet[ONE_MEMBERSHIP_TERM],
    1
  ]
  point2 = [
    x,
    w0
  ]
  [gradient, intercept] = calcGradientIntercept(point1, point2)
  newZeroMembershipTerm = (1-intercept) / gradient

  return newZeroMembershipTerm