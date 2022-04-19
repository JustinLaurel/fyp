from scipy.integrate import odeint
import numpy as numpy
import matplotlib.pyplot as plot
from math import exp
from services.helpers import *
from services.constants import *
import xlsxwriter
from sensor import Sensor

reactionIsOver = False
finalYield = None
temperatureHistory = []
sensor = Sensor(293, 2.8)
def odes(
  x, 
  t,
  initialTemp = 293, # K
  nitrogenFlow = 2.8,# m/s
  reactorHeight = 8
):
  global reactionIsOver
  global finalYield
  global temperatureHistory

  tungstenTemp = 2600

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
  solidMass = m1 + m2 + m3 + m4 + m5 + m6 + m9

  sensor.update(innerTemp, temperatureHistory, tungstenTemp, t)
  temperatureHistory.append({
    "innerTemp": innerTemp,
    "time": t
  })
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
  ]

# constants
biomassMass = 50
initialTemp = 293
nitrogenFlowrate = 2.8

timeRangeSeconds = 6
timeSteps = 1000


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
]

# time vector (time window)
t = numpy.linspace(0, timeRangeSeconds, timeSteps)
x = odeint(odes, x0, t, (initialTemp, nitrogenFlowrate))

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


#Write Sensor data to Excel
book = xlsxwriter.Workbook('pyrolyzer.xlsx')
sheet1 = book.add_worksheet('main')
sheet1.write(0, 0, 'Tungsten temp')
sheet1.write(0, 1, 'Sensor temp')
sheet1.write(0, 2, 'Inner temp')
sheet1.write(0, 3, 'Time')

rowIndex = 1
for log in innerTempLogs:
  sheet1.write(rowIndex, 0, tungstenTempLogs[rowIndex - 1])
  sheet1.write(rowIndex, 1, sensorTempLogs[rowIndex - 1])
  sheet1.write(rowIndex, 2, innerTempLogs[rowIndex - 1])
  sheet1.write(rowIndex, 3, timeLogs[rowIndex - 1])
  rowIndex += 1
book.close()


# Display the results
print('Final tar yield: ' + str(finalYield) + ' kg')
plot.subplot(2, 1, 1)
plot.xlabel('time (s)')
plot.ylabel('temperature (K)')
plot.title('Graph of actual temp, sensor temp & tungsten temp vs time')
plot.plot(timeLogs, innerTempLogs, label="Actual temperature")
plot.plot(timeLogs, sensorTempLogs, label="Sensor temperature")
plot.plot(timeLogs, tungstenTempLogs, label="Tungsten temperature")
plot.legend()
plot.ylim(0, 3400)

plot.subplot(2, 1, 2)
plot.xlabel('time (s)')
plot.ylabel('mass (kg)')
plot.title('Graph of composition change for biomass')
plot.plot(t, m1, label="cellulose")
plot.plot(t, m2, label="hemicellulose")
plot.plot(t, m3, label="lignin")
# plot.plot(t, m4, label="active cellulose")
# plot.plot(t, m5, label="active hemicellulose")
# plot.plot(t, m6, label="active lignin")
plot.plot(t, m7, label="tar")
plot.plot(t, m8, label="non-condensable gases")
plot.plot(t, m9, label="char")
annot_max(t, m7)
plot.legend()
plot.ylim(0, 55)
plot.show()

print('hello')