import numpy as numpy
import pandas as pandas
import matplotlib.pyplot as plot
from scipy.optimize import minimize
from scipy.interpolate import interp1d as interpolate
from scipy.integrate import odeint

file = pandas.ExcelFile(r'C:\Users\Spring\Desktop\Code\fyp\solver\stepResponse_2.xlsx')
rawData = pandas.read_excel(file, 'main').values

data = numpy.array(rawData)
data = data.transpose()

TUNGSTEN_DATA = 0
SENSOR_DATA = 1
ACTUAL_TEMP_DATA = 2
TIME_DATA = 3

tungstenData = data[TUNGSTEN_DATA]
actualTempData = data[ACTUAL_TEMP_DATA]
sensorData = data[SENSOR_DATA]
timeData = data[TIME_DATA]

initialTungstenTemp = tungstenData[0]
initialActualTemp = actualTempData[0]

tungstenHistory = interpolate(timeData, tungstenData)

gain = 1
timeConstant = 10
timeDelay = 0.4

def fopdt(tungstenTemp, t, tungstenHistory, gain, timeConstant, timeDelay):
  tungstenTempWithTimeDelay = initialTungstenTemp

  try:
    if (t - timeDelay) > 0: tungstenTempWithTimeDelay = tungstenHistory(t - timeDelay)
  except:
    tungstenTempWithTimeDelay = initialTungstenTemp

  dTactual_dt = (
    -(tungstenTemp - initialTungstenTemp) + \
    gain*(tungstenTempWithTimeDelay - initialTungstenTemp)
  ) / timeConstant

  return dTactual_dt

def simulateResponse(fopdt, initialTungstenTemp, timeData, args):
  tungstenHistory, gain, timeConstant, timeDelay = args
  return odeint(fopdt, [initialTungstenTemp], timeData, args=(
    tungstenHistory,
    gain,
    timeConstant,
    timeDelay
  ))

sensorValues = simulateResponse(fopdt, initialTungstenTemp, timeData, args=(
  tungstenHistory,
  gain,
  timeConstant,
  timeDelay
))


# Calculates sum of squares error
def objectiveFunction(constants):
  [gain, timeConstant, timeDelay] = constants
  simulatedSensorOutputs = odeint(fopdt, [initialTungstenTemp], timeData, args=(
    tungstenHistory,
    gain,
    timeConstant,
    timeDelay
  ))

  objectiveValue = 0
  actualSensorOutputs = sensorData
  for index in range(len(simulatedSensorOutputs)):
    objectiveValue += (
      simulatedSensorOutputs[index] - actualSensorOutputs[index]
    ) ** 2
  
  return objectiveValue

print('Initial sum of squares error: ' + str(
  objectiveFunction([gain, timeConstant, timeDelay])
))

optimizedConstants = minimize(objectiveFunction, [gain, timeConstant, timeDelay]).x

print('Optimized sum of squares error: ' + str(
  objectiveFunction(optimizedConstants)
))

initialGuessResponse = simulateResponse(fopdt, initialTungstenTemp, timeData, args=(
  tungstenHistory,
  gain,
  timeConstant,
  timeDelay
))
optimizedResponse = simulateResponse(
  fopdt,
  initialTungstenTemp,
  timeData,
  args=(tungstenHistory, *optimizedConstants)
)

plot.figure()
plot.subplot(2,1,1)
plot.plot(timeData, sensorData, label='Actual sensor temperature')
plot.plot(timeData, initialGuessResponse, label='FOPDT with initial guess')
plot.plot(timeData, optimizedResponse, label='FOPDT with optimized constants')
plot.ylabel('Sensor temperature (K)')
plot.xlabel('time (s)')
plot.legend(loc='best')
plot.subplot(2,1,2)
plot.plot(timeData, tungstenData)
plot.plot(timeData, tungstenHistory(timeData))
plot.legend(['Measured','Interpolated'],loc='best')
plot.ylabel('Tungsten temperature (K)')
plot.show()
