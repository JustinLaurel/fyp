from random import randint
from scipy.integrate import odeint
import numpy as numpy
import matplotlib.pyplot as plot
from math import exp
from services.helpers import *
from services.constants import *
import xlsxwriter
from ucMain import calcUc

nitrogenFlowrates = []  # kg/s
dieselFlowrates = []    # kg/s

stateAndOutput = [] #[(Final tar yield (kg)), (Actual residence time), heatingRate, mNitrogen]
maxYieldWithResidenceTime = [0, 0] #[(max yield), (t at max yield)]

outputValuesList = []
additionalDataList = []

def odes(
  x, 
  t,
  heatingRate = 150, # K/s
  initialTemp = 293, # K
  mNitrogen = 1.2, #kg/s
):
  currentTemp = initialTemp + (heatingRate * t)

  #Arrhenius rate constants
  k1c = a1 * exp(K1 / currentTemp)
  k2c = a2 * exp(K2 / currentTemp)
  k3c = a3 * exp(K3 / currentTemp)
  k1h = a4 * exp(K4 / currentTemp)
  k2h = a5 * exp(K5 / currentTemp)
  k3h = a6 * exp(K6 / currentTemp)
  k1l = a7 * exp(K7 / currentTemp)
  k2l = a8 * exp(K8 / currentTemp)
  k3l = a9 * exp(K9 / currentTemp)
  k4 = a10 * exp(K10 / currentTemp)


  # assign each ODE to a vector element
  m1 = x[0]
  m2 = x[1]
  m3 = x[2]
  m4 = x[3]
  m5 = x[4]
  m6 = x[5]
  m7 = x[6]
  m8 = x[7]
  m9 = x[8]

  # define each ODE
  dm1_dt = -k1c * m1
  dm2_dt = -k1h * m2
  dm3_dt = -k1l * m3
  dm4_dt = k1c*m1 - (k2c+k3c)*m4
  dm5_dt = k1h*m2 - (k2h+k3l)*m5
  dm6_dt = k1l*m3 - (k2l+k3l)*m6
  dm7_dt = k2c*m4 + k2h*m5 + k2l*m6 - k4*m7
  dm9_dt = (yc*k3c*m4 + yh*k3h*m5 + yl*k3l*m6 + (dm1_dt + dm2_dt + dm3_dt + dm4_dt + dm5_dt + dm6_dt)*(pg/pb) ) \
    / (1 + (pg/pb))
  dm8_dt = (1-yc)*k3c*m4 + (1-yh)*k3h*m5 + (1-yl)*k3l*m6 + k4*m7 - \
    (
      ((dm1_dt + dm2_dt + dm3_dt + dm4_dt + dm5_dt + dm6_dt) * (1/pb)) - \
      (dm9_dt * (1/pc)) \
    ) * pg

  mSolid = m1+m2+m3+m4+m5+m6+m9
  mDiesel = (3.6136*heatingRate - mNitrogen*heatingRate + mNitrogen*currentTemp - 293*mNitrogen + 1.3654*mSolid*heatingRate) / (42307.69 + 21*heatingRate - 21*currentTemp + 6153)

  nitrogenFlowrates.append(mNitrogen)
  dieselFlowrates.append(mDiesel)

  meanNitrogenFlowrate = getAverage(nitrogenFlowrates)
  meanDieselFlowrate = getAverage(dieselFlowrates)
  actualResidenceTime = (6.28) / (meanNitrogenFlowrate*1.701 + meanDieselFlowrate*35.84)

  if m7 > maxYieldWithResidenceTime[0]:
    maxYieldWithResidenceTime[0] = m7
    maxYieldWithResidenceTime[1] = t
  if (t > actualResidenceTime) & (len(stateAndOutput) == 0):
    stateAndOutput.append(m7)
    stateAndOutput.append(t)
    stateAndOutput.append(heatingRate)
    stateAndOutput.append(mNitrogen)
    stateAndOutput.append(mDiesel)

  return [
    dm1_dt, # Cellulose
    dm2_dt, # Hemicellulose
    dm3_dt, # Lignin
    dm4_dt, # Active Cellulose
    dm5_dt, # Active Hemicellulose
    dm6_dt, # Active Lignin
    dm7_dt, # Tar
    dm8_dt, # Gas
    dm9_dt, # Char
  ]

# constants
biomassMass = 1.5
timeRangeSeconds = 5
initialTemp = 293

# initial conditions
x0 = [  #Composition @ t=0, kg
  biomassMass * 0.42, #Cellulose
  biomassMass * 0.32, #Hemicellulose
  biomassMass * 0.26, #Lignin
  0,  #Active cellulose
  0,  #Active hemicellulose
  0,  #Active lignin
  0,  #Tar
  0,  #Gas
  0,  #Char
]

# time vector (time window)
t = numpy.linspace(0, timeRangeSeconds, 100)

nitrogenFlowrateLinspace = numpy.linspace(0.6, 1.2, 2500)

#Excel initialization
book = xlsxwriter.Workbook('Nitrogen_Flowrate.xlsx')
sheet1 = book.add_worksheet("dataset A")
sheet2 = book.add_worksheet("dataset B")
sheet3 = book.add_worksheet("main")
addTarHeaders(sheet1)
addTarHeaders(sheet2)
addTarHeaders(sheet3)
row1 = 1
row2 = 1
row3 = 1

alternatingIndex = 2
FINAL_TAR_YIELD = 0
RESIDENCE_TIME = 1
HEATING_RATE = 2
M_NITROGEN = 3
M_DIESEL = 4
datasetA = []
datasetB = []
heatingRate = 200 # heating rate at max yield 
for nitrogenFlowrate in nitrogenFlowrateLinspace:
  odeint(odes, x0, t, (heatingRate, initialTemp, nitrogenFlowrate))
  outputValuesList.append(stateAndOutput.copy())
  additionalDataList.append(maxYieldWithResidenceTime.copy())
  
  # Correction factor to discourage heating rates from exceeding 200degC
  # Because damaging effects of high heat fluxes on refractory & equipment are not accounted for
  finalTarYield = stateAndOutput[FINAL_TAR_YIELD]
  if heatingRate > 200:
    finalTarYield = stateAndOutput[FINAL_TAR_YIELD] * ((100-(heatingRate - 200)) / 100)

  #Write to excel
  if len(stateAndOutput) != 0:
    if (alternatingIndex % 2 == 0):
      sheet1.write(row1, 0, finalTarYield)
      sheet1.write(row1, 1, stateAndOutput[RESIDENCE_TIME])
      sheet1.write(row1, 2, stateAndOutput[HEATING_RATE])
      sheet1.write(row1, 3, stateAndOutput[M_NITROGEN])
      sheet1.write(row1, 4, stateAndOutput[M_DIESEL])

      datasetA.append([
        finalTarYield,
        stateAndOutput[HEATING_RATE],
        stateAndOutput[M_NITROGEN]
      ])

      row1 += 1
      alternatingIndex +=1
    else:
      sheet2.write(row2, 0, finalTarYield)
      sheet2.write(row2, 1, stateAndOutput[RESIDENCE_TIME])
      sheet2.write(row2, 2, stateAndOutput[HEATING_RATE])
      sheet2.write(row2, 3, stateAndOutput[M_NITROGEN])
      sheet2.write(row2, 4, stateAndOutput[M_DIESEL])

      datasetB.append([
        finalTarYield,
        stateAndOutput[HEATING_RATE],
        stateAndOutput[M_NITROGEN]
      ])

      row2 += 1
      alternatingIndex += 1

    sheet3.write(row3, 0, finalTarYield)
    sheet3.write(row3, 1, stateAndOutput[RESIDENCE_TIME])
    sheet3.write(row3, 2, stateAndOutput[HEATING_RATE])
    sheet3.write(row3, 3, stateAndOutput[M_NITROGEN])
    sheet3.write(row3, 4, stateAndOutput[M_DIESEL])
    row3 += 1

    #Reset values
    stateAndOutput = []
    maxYieldWithResidenceTime = [0, 0]
    nitrogenFlowrates = []
    dieselFlowrates = []
    print('rows processed: ' + str(row3))

book.close()
print(
  'uc = ' + str(calcUc(
    datasetA,
    datasetB
  ))
)
