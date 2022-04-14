import random
import numpy as numpy
import xlsxwriter
import pandas as pandas

from helpers import addHeatingRateHeaders
from uc.uc_main import calcUc

solidMassRange = [0, 1.5]
currentTempRange = [293, 1073]
heatingRateRange = [100, 240]
nitrogenFlowrateRange = [0.6, 1.2]
solidMassRange = [0, 1.5]
currentTempRange = [293, 1073]
DATASET_SIZE = 40000

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

book = xlsxwriter.Workbook('diesel_flow.xlsx')
sheet1 = book.add_worksheet("datasetA")
sheet2 = book.add_worksheet("datasetB")
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

for index in range(DATASET_SIZE):
  heatingRate = random.uniform(heatingRateRange[0], heatingRateRange[1])
  currentTemp = random.uniform(currentTempRange[0], currentTempRange[1])
  nitrogenFlowrate = random.uniform(nitrogenFlowrateRange[0], nitrogenFlowrateRange[1])
  solidMass = random.uniform(solidMassRange[0], solidMassRange[1])

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
  sheet3.write(row3, 0, dieselFlowrate)
  sheet3.write(row3, 1, heatingRate)
  sheet3.write(row3, 2, currentTemp)
  sheet3.write(row3, 3, nitrogenFlowrate)
  sheet3.write(row3, 4, solidMass)
  row3 += 1
  print('rows processed: ' + str(row3) + 'dieselFlowrate=' + str(dieselFlowrate))

book.close()
# print(
#   'uc = ' + str(calcUc(
#     datasetA,
#     datasetB
#   ))
# )
