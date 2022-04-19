import math
from scipy.integrate import odeint
from services.helpers import sortByTime

class Sensor():
  def __init__(self, initialTemp, nitrogenFlowrate):
    self.initialTemp = initialTemp
    self.sensorTemp = initialTemp
    self.nitrogenFlowrate = nitrogenFlowrate

    self.sensorDistanceFromTungsten = 1.12
    self.sensorTimeDelay = self.sensorDistanceFromTungsten / self.nitrogenFlowrate

    self.sensorLogs = []

  def computeChange(self, innerTemp, innerTempHistory, t):
    delay = self.sensorTimeDelay
    innerTempWithTimeDelay = 293 #Initial temperature

    for data in reversed(innerTempHistory):
      if data["time"] < (t - delay):
        innerTempWithTimeDelay = data["innerTemp"]
        break

    dTsensor_dt = (-self.sensorTemp + innerTempWithTimeDelay) / (0.7421*math.exp(0.0008*innerTemp))
    dTsensor_dtNoDelay = (-self.sensorTemp + innerTemp) / 5

    self.sensorTemp
    innerTempWithTimeDelay
    innerTemp
    return dTsensor_dt

  def update(self, innerTemp, innerTempHistory, tungstenTemp, t):
    dTsensor_dt = self.computeChange(innerTemp, innerTempHistory, t)
    change = 0
    if len(innerTempHistory) > 1:
      if t > innerTempHistory[-1]['time']:
        if (t > 126) & (innerTemp > 2900): return self.sensorTemp
        change = dTsensor_dt * (t-innerTempHistory[-1]['time'])
        print('sensorTemp change=' + str(change) + ', time=' + str(t))
        self.sensorTemp += change
        self.sensorLogs.append({"sensor": self.sensorTemp, "inner": innerTemp, "tungsten": tungstenTemp, "time": t})



    return self.sensorTemp

  def getReading(self):
    return self.sensorTemp

  def getLogs(self):
    return sortByTime(self.sensorLogs)
