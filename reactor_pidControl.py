from scipy.integrate import odeint
import numpy as numpy
import matplotlib.pyplot as plot
from math import exp
from services.helpers import *
from services.constants import *
from sensor import Sensor
from pid import PidController

reactionIsOver = False
tarYield = None
temperatureHistory = []
sensor = Sensor(293, 2.8)
def odes(
  x, 
  t,
  tungstenTemp,
  initialTemp = 293
):
  global reactionIsOver
  global tarYield
  global temperatureHistory

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

# constants
biomassMass = 50
initialTemp = 293
nitrogenFlowrate = 2.8

timeRangeSeconds = 5
timeSteps = 1000


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

# time vector (time window)
timeSteps = numpy.linspace(0, timeRangeSeconds, timeSteps)

currentStates = initialStates
tungstenTemp = 3000
tungstenTemps = numpy.ones(len(timeSteps)) * tungstenTemp

reactorHeight = 8
nitrogenFlow = 2.8

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
tarYield = None

tungstenTemps = numpy.zeros(len(timeSteps))
sensorTemps = numpy.zeros(len(timeSteps))
errors = numpy.zeros(len(timeSteps))
integralErrors = numpy.zeros(len(timeSteps))
derivativeFeedbacks = numpy.zeros(len(timeSteps))
setpoints = numpy.ones(len(timeSteps))

sensorSetpointIncreaseRate = 111.67
for index in range(len(setpoints)):
  setpoints[index] = timeSteps[index] * sensorSetpointIncreaseRate + 293

maxTungstenTemp = 3200
minTungstenTemp = 293

sensorTemps[0] = 293

controller = PidController()
controller.setParams(10, 0.3, 0.1)

for index in range(len(timeSteps) - 1):
  deltaTime = timeSteps[index+1] - timeSteps[index]
  errors[index] = setpoints[index] - sensorTemps[index]
  error = errors[index]
  if index >= 1:
    derivativeFeedbacks[index] = (sensorTemps[index] - sensorTemps[index-1]) / deltaTime
    integralErrors[index] = integralErrors[index-1] + errors[index] * deltaTime

  evaluated = controller.evaluate(
    tungstenTemps[0],
    errors[index],
    integralErrors[index],
    derivativeFeedbacks[index]
  )
  tungstenTemps[index] = evaluated

  if tungstenTemps[index] > maxTungstenTemp:
    tungstenTemps[index] = maxTungstenTemp
    integralErrors[index] = integralErrors[index] - errors[index] * deltaTime
  elif tungstenTemps[index] < minTungstenTemp:
    tungstenTemps[index] = minTungstenTemp
    integralErrors[index] = integralErrors[index] - errors[index] * deltaTime

  currentTimeStep = [
    timeSteps[index],
    timeSteps[index + 1]
  ]
  output = odeint(odes, currentStates, currentTimeStep, args=(
    tungstenTemps[index],
    293
  ))[-1]

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

  sensorTemp = sensor.update(
    actualTemp[index+1],
    temperatureHistory,
    tungstenTemps[index],
    timeSteps[index]
  )
  sensorTemps[index+1] = sensor.getReading()

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

  temperatureHistory.append({
    "innerTemp": actualTemp[index + 1],
    "time": currentTimeStep[0]
  })
  print('actualTemp:' + str(actualTemp[index]) + 'K, tungstenTemp: ' + str(tungstenTemp) + 'K, sensorTemp: ' + str(sensorTemp) + ', time: ' + str(currentTimeStep[0]) + 's')
  
  if (reactionIsOver is False) & (currentTimeStep[0] > reactorHeight/nitrogenFlow):
    tarYield = {"yield": m7[index], "time": currentTimeStep[0]}
    reactionIsOver = True
    # break

# Retrieve data from Sensor
logs = sensor.getLogs()
innerTempLogs = []
sensorTempLogs = []
tungstenTempLogs = []
timeLogs = []
for log in logs:
  innerTempLogs.append(log["inner"])
  sensorTempLogs.append(log["sensor"])
  tungstenTempLogs.append(log["tungsten"])
  timeLogs.append(log["time"])
  # print('sensor temp=' + str(log['sensor']) + ', time=' + str(log['time']))

controllerLogs = controller.getLogs()
controllerParams = controller.getParams()


# Display the results
print('Final tar yield: ' + str(tarYield['yield']) + ' kg, at t=' + str(tarYield['time']))
plot.subplot(2, 1, 1)
plot.xlabel('time (s)')
plot.ylabel('temperature (K)')
plot.title('P-term: 10, I-term: 0.3, D-term: 0.1')
# plot.plot(timeLogs, innerTempLogs, label="Actual temperature")
plot.plot(timeLogs, sensorTempLogs, label="Sensor temperature")
plot.plot(timeSteps, setpoints, label="Setpoint sensor")
plot.plot(timeLogs, tungstenTempLogs, label="Tungsten temperature")
plot.legend()
plot.ylim(0, 3400)

plot.subplot(2, 1, 2)
plot.xlabel('time (s)')
plot.ylabel('mass (kg)')
plot.title('Graph of composition change for biomass')
plot.plot(timeSteps, m1, label="cellulose")
plot.plot(timeSteps, m2, label="hemicellulose")
plot.plot(timeSteps, m3, label="lignin")
# plot.plot(t, m4, label="active cellulose")
# plot.plot(t, m5, label="active hemicellulose")
# plot.plot(t, m6, label="active lignin")
plot.plot(timeSteps, m7, label="tar")
plot.plot(timeSteps, m8, label="non-condensable gases")
plot.plot(timeSteps, m9, label="char")
annot_max(timeSteps, m7)
# plot.legend()
plot.ylim(0, 52)
plot.show()

print('hello')