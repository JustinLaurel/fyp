import numpy as numpy
import xlsxwriter
import pandas as pandas

from helpers import addHeatingRateHeaders
from uc.uc_main import calcUc

mainDataLinspace = [18, 12, 12, 12, 32]
reducedSizeDataLinspace = [14, 5, 5, 5, 20]

# dieselFlowrateLinspace = numpy.linspace(0.0020, .053, 24)
heatingRateLinspace = numpy.linspace(110, 240, 24)
nitrogenFlowrateLinspace = numpy.linspace(0.6, 1.2, 5)
solidMassLinspace = numpy.linspace(0, 1.5, 7)
currentTempLinspace = numpy.linspace(293, 1073,  30)

def calcDieselFlow(
  heatingRate,
  currentTemp,
  nitrogenFlowrate,
  solidMass,
):
  return (
    (
      nitrogenFlowrate*currentTemp - 293*nitrogenFlowrate + 3.6136*heatingRate - nitrogenFlowrate*heatingRate + 1.3654*solidMass*heatingRate
    ) / (
      42307.69 - 21*currentTemp + 6153 + 21*heatingRate
    )
  )

book = xlsxwriter.Workbook('solid.xlsx')
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
  for heatingRate in heatingRateLinspace:
    for nitrogenFlowrate in nitrogenFlowrateLinspace:
      for solidMass in solidMassLinspace:
        dieselFlowrate = calcDieselFlow(heatingRate, currentTemp, nitrogenFlowrate, solidMass)
        
        if (alternatingIndex % 2 == 0):
          sheet1.write(row1, 0, dieselFlowrate)
          sheet1.write(row1, 1, heatingRate)
          sheet1.write(row1, 2, currentTemp)
          sheet1.write(row1, 3, nitrogenFlowrate)
          sheet1.write(row1, 4, solidMass)

          datasetA.append([
            dieselFlowrate,
            heatingRate,
            currentTemp,
            nitrogenFlowrate,
            solidMass,
          ])

          row1 += 1
        else:
          sheet2.write(row2, 0, dieselFlowrate)
          sheet2.write(row2, 1, heatingRate)
          sheet2.write(row2, 2, currentTemp)
          sheet2.write(row2, 3, nitrogenFlowrate)
          sheet2.write(row2, 4, solidMass)

          datasetB.append([
            dieselFlowrate,
            heatingRate,
            currentTemp,
            nitrogenFlowrate,
            solidMass,
          ])

          row2 += 1

        alternatingIndex +=1
        sheet3.write(row1, 0, dieselFlowrate)
        sheet3.write(row1, 1, heatingRate)
        sheet3.write(row1, 2, currentTemp)
        sheet3.write(row1, 3, nitrogenFlowrate)
        sheet3.write(row1, 4, solidMass)
        row3 += 1

        print('rows processed: ' + str(row3) + 'dieselFlowrate=' + str(dieselFlowrate))

book.close()
# print(
#   'uc = ' + str(calcUc(
#     datasetA,
#     datasetB
#   ))
# )
