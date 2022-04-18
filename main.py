print('hello')
from random import randint
from scipy.integrate import odeint
from scipy.integrate import quad
import numpy as numpy
import matplotlib.pyplot as plot
from math import exp
# from heatingRate.dieselFuzzySets import modelEvaluate
from services.helpers import *
from services.constants import *
import xlsxwriter
from ucMain import calcUc

reactionIsOver = False
finalYield = None
temperatureHistory = []
def odes(
  x, 
  t,
  desiredHeatingRate = 200, # K/s
  initialTemp = 293, # K
  nitrogenFlow = 2.8,# m/s
  reactorHeight = 8
):
  global reactionIsOver
  global finalYield
  global temperatureHistory

  sensorDistanceFromTungsten = 1.12
  sensorTimeDelay = sensorDistanceFromTungsten / nitrogenFlow

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
  innerTemp = x[9]
  sensorTemp = x[10]

  # sensorTemp = initialTemp
  # sensorDistanceFromTungsten = 1.12
  # sensorTimeDelay = sensorDistanceFromTungsten / nitrogenFlow

  # for data in reversed(temperatureHistory):
  #   if data["time"] < (t - sensorTimeDelay): 
  #     sensorTemp = data["innerTemp"]
  #     break

  innerTempWithTimeDelay = initialTemp
  for data in reversed(temperatureHistory):
    if data["time"] < (t-sensorTimeDelay):
      innerTempWithTimeDelay = data["innerTemp"]
      break


  temperatureHistory.append({
    "innerTemp": innerTemp,
    "time": t
  })

  print('sensorTemp=' + str(sensorTemp) + ', innerTemp=' + str(innerTemp) + ', t=' + str(t))


  solidMass = m1 + m2 + m3 + m4 + m5 + m6 + m9

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

  # tungstenTemp = pidEvaluateTungsten(innerTemp)
  tungstenTemp = 3000

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
  dTsensor_dt = (
    (-sensorTemp + innerTempWithTimeDelay) / (0.0004*innerTemp**0.8725)
  )

  if (not reactionIsOver) & (t > reactorHeight/nitrogenFlow):
    finalYield = m7
    reactionIsOver = True

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
    dTsensor_dt # sensorTemp, Thermocouple temperature
  ]

# constants
biomassMass = 70
timeRangeSeconds = 10
heatingRate = 200
mNitrogen = 0.8

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
  293, #Initial inner temperature
  293, #Initial sensor temperature
]

# time vector (time window)
t = numpy.linspace(0, timeRangeSeconds, 100)
x = odeint(odes, x0, t, (heatingRate, 293))

m1 = x[:, 0]
m2 = x[:, 1]
m3 = x[:, 2]
m4 = x[:, 3]
m5 = x[:, 4]
m6 = x[:, 5]
m7 = x[:, 6]
m8 = x[:, 7]
m9 = x[:, 8]
innerTemp = x[:, 9]
sensorTemp = x[:, 10]

#Excel initialization
book = xlsxwriter.Workbook('Input_Output.xlsx')
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
datasetA = []
datasetB = []

ax = plot.subplots()

# Display the results
print('Final tar yield: ' + str(finalYield) + ' kg')
plot.subplot(2, 1, 1)
plot.xlabel('time (s)')
plot.ylabel('temperature (K)')
plot.title('Graph of inner and sensor temperature vs time')
plot.plot(t, innerTemp, label="Inner temperature")
plot.plot(t, sensorTemp, label="Sensor temp")
plot.legend()
plot.ylim(0, 1500)


plot.subplot(2, 1, 2)
plot.xlabel('time (s)')
plot.ylabel('mass (kg)')
plot.title('Graph of composition change for biomass')
plot.plot(t, m1, label="cellulose")
plot.plot(t, m2, label="hemicellulose")
plot.plot(t, m3, label="lignin")
plot.plot(t, m7, label="tar")
plot.plot(t, m9, label="char")
annot_max(t, m7)
plot.legend()
plot.ylim(0, 70)

plot.show()
print('hello')