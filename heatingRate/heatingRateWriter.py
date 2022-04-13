import numpy as numpy
import xlsxwriter
import pandas as pandas

from helpers import addHeatingRateHeaders
from uc.uc_main import calcUc

mainDataLinspace = [18, 12, 12, 12, 32]
reducedSizeDataLinspace = [14, 5, 5, 5, 20]

dieselFlowrateLinspace = numpy.linspace(0.0020, .053, 18)
nitrogenFlowrateLinspace = numpy.linspace(0.6, 1.2, 3)
biomassLinspace = numpy.linspace(0, 1.5, 5)
charLinspace = numpy.linspace(0, 0.3, 5)
currentTempLinspace = numpy.linspace(293, 1073, 24)

stateAndOutput = []
HEATING_RATE = 0
M_DIESEL = 1
M_NITROGEN = 2
BIOMASS_MASS = 3
CHAR_MASS = 4

def calcHeatingRate(
  currentTemp,
  mDiesel,
  mNitrogen,
  biomassMass,
  charMass
):
  return (
    (42307.69*mDiesel - 21*mDiesel*currentTemp + 6153*mDiesel - mNitrogen*currentTemp + 293*mNitrogen)
    / (3.6136 - 21*mDiesel - mNitrogen + 1.3654*biomassMass + charMass*(0.96462+0.00201*(currentTemp-293)))
  )


book = xlsxwriter.Workbook('main.xlsx')
sheet1 = book.add_worksheet("dataset A")
sheet2 = book.add_worksheet("dataset B")
sheet3 = book.add_worksheet("main")
addHeatingRateHeaders(sheet1)
addHeatingRateHeaders(sheet2)
addHeatingRateHeaders(sheet3)

row1 = 1
row2 = 1
row3 = 1
alternatingIndex = 2
datasetA = []
datasetB = []
for currentTemp in currentTempLinspace:
  for diesel in dieselFlowrateLinspace:
    for nitrogen in nitrogenFlowrateLinspace:
      for biomass in biomassLinspace:
        for char in charLinspace:
          heatingRate = calcHeatingRate(currentTemp, diesel, nitrogen, biomass, char)
          
          if (alternatingIndex % 2 == 0):
            sheet1.write(row1, 0, heatingRate)
            sheet1.write(row1, 1, currentTemp)
            sheet1.write(row1, 2, diesel)
            sheet1.write(row1, 3, nitrogen)
            sheet1.write(row1, 4, biomass)
            sheet1.write(row1, 5, char)

            datasetA.append([
              heatingRate,
              currentTemp,
              diesel,
              nitrogen,
              biomass,
              char
            ])

            row1 += 1
          else:
            sheet2.write(row2, 0, heatingRate)
            sheet2.write(row2, 1, currentTemp)
            sheet2.write(row2, 2, diesel)
            sheet2.write(row2, 3, nitrogen)
            sheet2.write(row2, 4, biomass)
            sheet2.write(row2, 5, char)

            datasetB.append([
              heatingRate,
              currentTemp,
              diesel,
              nitrogen,
              biomass,
              char
            ])

            row2 += 1

          alternatingIndex +=1
          sheet3.write(row3, 0, heatingRate)
          sheet3.write(row3, 1, currentTemp)
          sheet3.write(row3, 2, diesel)
          sheet3.write(row3, 3, nitrogen)
          sheet3.write(row3, 4, biomass)
          sheet3.write(row3, 5, char)
          row3 += 1

          print('rows processed: ' + str(row3) + 'heatingRate=' + str(heatingRate))

book.close()
# print(
#   'uc = ' + str(calcUc(
#     datasetA,
#     datasetB
#   ))
# )





