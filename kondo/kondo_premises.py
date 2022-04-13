import math
import numpy
import pandas as pandas
from helpers import *

file = pandas.ExcelFile(r'C:\Users\Spring\Desktop\heatingRateModel\kondo.xlsx')
data = pandas.read_excel(file, 'main').values

X1_INDEX = 0
X2_INDEX = 1
X3_INDEX = 2
X4_INDEX = 3
OUTPUT_INDEX = 4

ZERO_MEMBERSHIP_TERM = 2  # Index of x value where degree of membership starts being zero
ONE_MEMBERSHIP_TERM = 1   # Index of x value where degree of membership starts being one
TERMINATE_TERM = 0        # Index where function terminates

WM_GRADIENT = 0

def calcY1(x1=0, x2=0, x3=0, x4=0):
  intercept = 20.7
  x1Coef = 2.153
  x2Coef = -1.599
  x3Coef = -4.528
  x4Coef = -0.143
  return intercept + x1Coef*x1 + x2Coef*x2 + x3Coef*x3 + x4Coef*x4
def calcY2(x1=0, x2=0, x3=0, x4=0):
  intercept = 21.2
  x1Coef = 1.86
  x2Coef = -1.161
  x3Coef = -2.576
  x4Coef = -0.399
  return intercept + x1Coef*x1 + x2Coef*x2 + x3Coef*x3 + x4Coef*x4

def calcMemberships(x, fuzzySets):
  memberships = []
  RULE_1 = 0
  RULE_2 = 1

  for fuzzySet in fuzzySets:
    point1 = [fuzzySet[ZERO_MEMBERSHIP_TERM], 0]
    point2 = [fuzzySet[ONE_MEMBERSHIP_TERM], 1]

    [gradient, intercept] = calcGradientIntercept(point1, point2)
    isDescendingFunction = gradient < 0

    if isDescendingFunction:
      if (x < fuzzySet[ONE_MEMBERSHIP_TERM]): memberships.append(1)
      elif (x > fuzzySet[ZERO_MEMBERSHIP_TERM]): memberships.append(0)
      else: memberships.append(gradient + intercept)

    elif not isDescendingFunction:
      if (x > fuzzySet[ONE_MEMBERSHIP_TERM]): memberships.append(1)
      elif (x < fuzzySet[ZERO_MEMBERSHIP_TERM]): memberships.append(2)
      else: memberships.append(gradient + intercept)
    

  if (x < 2.5): memberships[RULE_1] = 1
  elif (x > 3.5): memberships[RULE_1] = 0
  else:
    memberships[RULE_1] = (-x + 3.5)

  if (x > 3.5): memberships[RULE_2] = 1
  elif (x < 2.5): memberships[RULE_2] = 0
  else:
    memberships[RULE_2] = (x - 2.5)

  return memberships

#membershipPoint: Degrees of membership
#dataY: Output from input-output data
#inferredY: Array of output from rules, from identified consequent parameter equations
def calcWmWnGradients(membershipPoint, dataY, inferredY):
  wmCoefficientTerm1 = dataY
  wnCoefficientTerm1 = dataY

  wmCoefficientTerm2 = inferredY[0]
  wnCoefficientTerm2 = inferredY[1]

  wmCoefficient = wmCoefficientTerm1 - wmCoefficientTerm2
  wnCoefficient = wnCoefficientTerm1 - wnCoefficientTerm2

  #wmGradient: gradient of function 'wn=wmGradient*wm'
  #wnGradient: gradient of function 'wm=wnGradient*wn'
  wmGradient = -wmCoefficient / wnCoefficient
  wnGradient = -wnCoefficient / wmCoefficient
  return [wmGradient, wnGradient]

def findClosestInterceptPoint(funcData, initialPoint):
  gradient = funcData[0]
  intercept = funcData[1]

  if 1+gradient == 0: return None

  wm1 = (0.7-intercept) / (1+gradient)
  wm2 = (1-intercept) / (1+gradient)

  wn1 = -wm1 + 0.7
  wn2 = -wm2 + 1

  intercept1 = [wm1, wn1]
  intercept2 = [wm2, wn2]

  closestIntercept = intercept1 if (
    calcDistanceBetweenPoints(initialPoint, intercept1) < calcDistanceBetweenPoints(initialPoint, intercept2)
  ) else intercept2

  return closestIntercept

def calcTildes(starPoint, membershipPoint):
  wmStar = starPoint[0]
  wnStar = starPoint[1]
  wm0 = membershipPoint[0]
  wn0 = membershipPoint[1]

  alpha1 = math.sqrt(1/2)
  alpha2M = 1 / (
    1 + abs(wmStar - wm0)
  )
  alpha2N = 1 / (
    1 + abs(wnStar - wn0)
  )
  
  alphaM = alpha1 * alpha2M
  alphaN = alpha1 * alpha2N

  wmTilde = wm0 + alphaM*(wmStar - wm0)
  wnTilde = wn0 + alphaN*(wnStar - wn0)
  return [wmTilde, wnTilde]

def calcLowerDeltaP(wTilde, beta, x, p):
  return wTilde * beta * abs(x-p)
def calcHigherDeltaP(wTilde, w0, beta, x, p):
  return (w0-wTilde) * beta * abs(x - p)





fuzzySetsX3 = [
  [0, 2.5, 3.5],
  [5, 3.5, 2.5]
]
SELECTED_X = X3_INDEX
L = 5 # Anywhere between 2*Range and 1*Range
print(str(fuzzySetsX3))

for datum in data:
  x1 = datum[X1_INDEX]
  x2 = datum[X2_INDEX]
  x3 = datum[X3_INDEX]
  x4 = datum[X4_INDEX]
  y0 = datum[OUTPUT_INDEX]

  selectedX = datum[SELECTED_X]
  selectedFuzzySet = fuzzySetsX3

  [wm0, wn0] = calcMemberships(selectedX, selectedFuzzySet)

  y1 = calcY1(x1, x2, x3)
  y2 = calcY2(x1, x2, x3)

  wmWnGradients = calcWmWnGradients(
    [wm0, wn0],
    y0,
    [y1, y2]
  )

  gradient = wmWnGradients[0]
  wnGradient = wmWnGradients[1] #wnGradient not really used
  intercept = 0

  #Calculate wmStar & wnStar
  closestPoint = getClosestPointOnFunction(
    [wm0, wn0],
    [gradient, intercept]
  )

  wmStar = None
  wnStar = None
  if (
    (closestPoint[0] + closestPoint[1]) >= 0.7
  ) & (
    closestPoint[0] + closestPoint[1] <= 1
  ): 
    wmStar = closestPoint[0]
    wnStar = closestPoint[1]
  
  else:
    intercept = findClosestInterceptPoint(
      [gradient, intercept],
      [wm0, wn0]
    )
    if intercept is None: continue #No fuzzy variables are modified for this data row

    wmStar = intercept[0]
    wnStar = intercept[1]
  #wmStar & wnStar calculations end here

  [wmTilde, wnTilde] = calcTildes(
    [wmStar, wnStar],
    [wm0, wn0]
  )

  # fuzzy set parameter adjustment starts here

  if (wm0 == 0) | (wn0 == 0):
    #Calculate beta
    pWithZeroMembership = None
    if (wm0 == 0): pWithZeroMembership = selectedFuzzySet[0][ZERO_MEMBERSHIP_TERM]
    else: pWithZeroMembership = selectedFuzzySet[1][ZERO_MEMBERSHIP_TERM]

    beta = (1 - abs(selectedX - pWithZeroMembership)/L) ** 3
    #beta calculations end 

    deltaPm = None
    deltaPn = None
    if (wm0 == 0):
      pm = selectedFuzzySet[0][ZERO_MEMBERSHIP_TERM]
      pn = selectedFuzzySet[1][ONE_MEMBERSHIP_TERM]
      deltaPm = calcLowerDeltaP(wmTilde, beta, selectedX, pm)
      deltaPn = calcHigherDeltaP(wnTilde, wn0, beta, selectedX, pn)

      selectedFuzzySet[0][ZERO_MEMBERSHIP_TERM] += deltaPm
      selectedFuzzySet[1][ONE_MEMBERSHIP_TERM] += deltaPn
      print('hello')
    elif (wn0 == 0):
      pm = selectedFuzzySet[0][ONE_MEMBERSHIP_TERM]
      pn = selectedFuzzySet[1][ZERO_MEMBERSHIP_TERM]
      deltaPm = calcHigherDeltaP(wmTilde, wm0, beta, selectedX, pm)
      deltaPn = calcLowerDeltaP(wnTilde, beta, selectedX, pn)

      selectedFuzzySet[0][ONE_MEMBERSHIP_TERM] += deltaPm
      selectedFuzzySet[1][ZERO_MEMBERSHIP_TERM] += deltaPn
      print('hi')
  
  # # if (wm0 != 0) & (wn0 != 0):
  # else: #Both wm0 and wn0 are > 0
  #   wmNewMembershipTerm = calcNewOneMembershipTerm(
  #     selectedFuzzySet[0],
  #     selectedX,
  #     wmTilde
  #   )
  #   wnNewMembershipTerm = calcNewOneMembershipTerm(
  #     selectedFuzzySet[1],
  #     selectedX,
  #     wnTilde
  #   )

  #   if (wmTilde >= 0.5): selectedFuzzySet[0][ONE_MEMBERSHIP_TERM] = wmNewMembershipTerm
  #   elif (wmTilde < 0.5): selectedFuzzySet[0][ZERO_MEMBERSHIP_TERM] = wmNewMembershipTerm

  #   if (wnTilde >= 0.5): selectedFuzzySet[1][ONE_MEMBERSHIP_TERM] = wnNewMembershipTerm
  #   elif(wnTilde < 0.5): selectedFuzzySet[1][ZERO_MEMBERSHIP_TERM] = wnNewMembershipTerm


  # fuzzy set parameter adjustment ends here

print(str(fuzzySetsX3))
