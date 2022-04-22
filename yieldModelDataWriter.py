import random
from scipy.integrate import odeint
import numpy as numpy
from math import exp
from services.helpers import addModelYieldHeaders
from services.helpers import *
from services.constants import *
from sensor import Sensor
import xlsxwriter

DATASET_SIZE = 20
tungstenHeatingRateRange = [700, 2000]
biomassMassRange = [25, 60]

# constants
# tungstenHeatingRate = 2000
# biomassMass = 60

initialTemp = 293
nitrogenFlowrate = 2.8

timeRangeSeconds = 6
timeSteps = 500

reactionIsOver = False
tarYield = None
temperatureHistory = []

def odes(
  x, 
  t,
  tungstenTemp,
  initialTemp = 293
):
  global reactionIsOver
  global tarYield
  global temperatureHistory

  if tungstenTemp == 0: tungstenTemp = initialTemp
  for i in range(len(x)):
    if (x[i] < 0) & (i != 9): x[i] = 0
    if (i == 9) & (x[i] > tungstenTemp): 
      x[i] = tungstenTemp

  m1 = x[0]
  m2 = x[1]
  m3 = x[2]
  m4 = x[3]
  m5 = x[4]
  m6 = x[5]
  m7 = x[6]
  m8 = x[7]
  m9 = x[8]
  innerTemp = x[9]
  solidMass = m1 + m2 + m3 + m4 + m5 + m6 + m9

  # print('sensorTemp=' + str(sensor.getReading()) + ', innerTemp=' + str(innerTemp) + ', t=' + str(t))

  k1c = a1 * exp(K1 / innerTemp)
  k2c = a2 * exp(K2 / innerTemp)
  k3c = a3 * exp(K3 / innerTemp)
  k1h = a4 * exp(K4 / innerTemp)
  k2h = a5 * exp(K5 / innerTemp)
  k3h = a6 * exp(K6 / innerTemp)
  k1l = a7 * exp(K7 / innerTemp)
  k2l = a8 * exp(K8 / innerTemp)
  k3l = a9 * exp(K9 / innerTemp)
  k4 = a10 * exp(K10 / innerTemp)

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
  dT_dt = (
    ((4.7156*innerTemp**2 + 628.711*innerTemp)*(tungstenTemp - innerTemp) + ((0.00006*innerTemp + 0.08)**0.43)*(-823500*innerTemp + 823500*293)) / 
    (((0.00006*innerTemp+0.08)**0.43) * (2351916 + 1420*solidMass*innerTemp))
  )
  # if (innerTemp >= tungstenTemp): 
  #   dT_dt = 0

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
    dT_dt,  # innerTemp, Reactor temperature
  ]


reactorHeight = 8
nitrogenFlow = 2.8

book = xlsxwriter.Workbook('yield_data.xlsx')
sheet1 = book.add_worksheet("datasetA")
sheet2 = book.add_worksheet("datasetB")
sheet3 = book.add_worksheet("main")
addModelYieldHeaders(sheet1)
addModelYieldHeaders(sheet2)
addModelYieldHeaders(sheet3)
row1 = 1
row2 = 1
row3 = 1
alternatingIndex = 2
datasetA = []
datasetB = []

# time vector (time window)
timeSteps = numpy.linspace(0, timeRangeSeconds, timeSteps)

for index in range(DATASET_SIZE):
  biomassMass = random.uniform(biomassMassRange[0], biomassMassRange[1])
  tungstenHeatingRate = random.uniform(tungstenHeatingRateRange[0], tungstenHeatingRateRange[1])
  
  # initial conditions
  initialStates = [  #Composition @ t=0, kg
    biomassMass * 0.42, #Cellulose
    biomassMass * 0.32, #Hemicellulose 
    biomassMass * 0.26, #Lignin
    0,  #Active cellulose
    0,  #Active hemicellulose
    0,  #Active lignin
    0,  #Tar
    0,  #Gas
    0,  #Char
    293, #Initial inner temperature
  ]


  currentStates = initialStates

  m1 = numpy.ones(len(timeSteps)) * initialStates[0]
  m2 = numpy.ones(len(timeSteps)) * initialStates[1]
  m3 = numpy.ones(len(timeSteps)) * initialStates[2]
  m4 = numpy.ones(len(timeSteps)) * initialStates[3]
  m5 = numpy.ones(len(timeSteps)) * initialStates[4]
  m6 = numpy.ones(len(timeSteps)) * initialStates[5]
  m7 = numpy.ones(len(timeSteps)) * initialStates[6]
  m8 = numpy.ones(len(timeSteps)) * initialStates[7]
  m9 = numpy.ones(len(timeSteps)) * initialStates[8]
  actualTemp = numpy.ones(len(timeSteps)) * initialStates[9]

  sensor = Sensor(293, 2.8)
  reactionIsOver = False
  tarYield = {'yield': 0, 'time': 0}

  maxTungstenTemp = 3200
  minTungstenTemp = 293

  temperatureHistory = []
  for index in range(len(timeSteps) - 1):
    deltaTime = timeSteps[index+1] - timeSteps[index]

    tungstenTemp = initialTemp + tungstenHeatingRate * timeSteps[index]

    if (tungstenTemp > maxTungstenTemp): tungstenTemp = maxTungstenTemp
    if (tungstenTemp < minTungstenTemp): tungstenTemp = minTungstenTemp


    currentTimeStep = [
      timeSteps[index],
      timeSteps[index + 1]
    ]
    output = odeint(odes, currentStates, currentTimeStep, args=(
      tungstenTemp,
      293
    ))[-1]
    sensor.update(actualTemp[index], temperatureHistory, tungstenTemp, timeSteps[index - 1])
    temperatureHistory.append({'innerTemp': actualTemp[index], 'time': timeSteps[index - 1]})

    m1[index+1] = output[0]
    m2[index+1] = output[1]
    m3[index+1] = output[2]
    m4[index+1] = output[3]
    m5[index+1] = output[4]
    m6[index+1] = output[5]
    m7[index+1] = output[6]
    m8[index+1] = output[7]
    m9[index+1] = output[8]
    actualTemp[index+1] = output[9]


    currentStates[0] = output[0]
    currentStates[1] = output[1]
    currentStates[2] = output[2]
    currentStates[3] = output[3]
    currentStates[4] = output[4]
    currentStates[5] = output[5]
    currentStates[6] = output[6]
    currentStates[7] = output[7]
    currentStates[8] = output[8]
    currentStates[9] = output[9]

    if (reactionIsOver is False) & (currentTimeStep[0] > reactorHeight/nitrogenFlow):
      tarYield = {"yield": m7[index], "time": currentTimeStep[0]}
      reactionIsOver = True
      break

    solidMass = output[0] + output[1] + output[2] + output[3] + output[4] + output[5] + output[8]
    if (solidMass <= 0.2*biomassMass): reactionIsOver = True


    if reactionIsOver is True: break

  finalSensorTemp = sensor.getLogs()[-1]['sensor']
  finalTime = sensor.getLogs()[-1]['time']

  sensorHeatingRate = (finalSensorTemp-293)/finalTime

  # Write to excel
  yieldPercent = tarYield['yield'] / biomassMass
  if (alternatingIndex % 2 == 0):
    sheet1.write(row1, 0, tarYield['yield'])
    sheet1.write(row1, 1, yieldPercent)
    sheet1.write(row1, 2, tungstenHeatingRate)
    sheet1.write(row1, 3, biomassMass)

    datasetA.append([tarYield, yieldPercent, tungstenHeatingRate, biomassMass])
    row1 += 1
  else:
    sheet2.write(row2, 0, tarYield['yield'])
    sheet2.write(row2, 1, yieldPercent)
    sheet2.write(row2, 2, tungstenHeatingRate)
    sheet2.write(row2, 3, biomassMass)

    datasetB.append([tarYield, yieldPercent, tungstenHeatingRate, biomassMass])
    row2 += 1

  alternatingIndex += 1
  sheet3.write(row3, 0, tarYield['yield'])
  sheet3.write(row3, 1, yieldPercent)
  sheet3.write(row3, 2, tungstenHeatingRate)
  sheet3.write(row3, 3, biomassMass)
  row3 += 1

  print('rows processed: ' + str(row3))

  # Reset globals
  reactionIsOver = False
  tarYield = {'yield': 0, 'time': 0}
  temperatureHistory = []

book.close()

print('hello')