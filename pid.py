class PidController():
  def __init__(self, gain = None, integralConstant = None, derivativeConstant = None):
    self.logs = []
    if (gain is not None):
      self.gain = gain
      self.integralConstant = integralConstant
      self.derivativeConstant = derivativeConstant

    
  def getParams(self):
    if self.gain is None: raise Exception('PID controller parameters are not defined')
    return [
      self.gain,
      self.integralConstant,
      self.derivativeConstant
    ]

  def identifyParams(self, gainP, timeConstantP, timeDelayP, hasDerivative = False):
    self.gain = (0.586/gainP) * ((timeDelayP / timeConstantP) ** -0.916)
    self.integralConstant = timeConstantP / (1.03 - 0.165*(timeDelayP / timeConstantP))
    self.derivativeConstant = None

    if hasDerivative is True: 
      self.derivativeConstant = (timeConstantP * timeDelayP) / (2*timeConstantP + timeDelayP)

    return [
      self.gain,
      self.integralConstant,
      self.derivativeConstant
    ]

  def setParams(self, gain, integralConstant, derivativeConstant = None):
    self.gain = gain
    self.integralConstant = integralConstant
    self.derivativeConstant = derivativeConstant

  def evaluate(self, initialOutput, error, integralError, differentialError):
    proportional = self.gain * error
    integral = self.gain / self.integralConstant * integralError
    derivative = 0
    if self.derivativeConstant is not None: 
      derivative = -self.gain * self.derivativeConstant * differentialError
    
    output = initialOutput + proportional + integral + derivative
    self.logs.append([output, proportional, integral, derivative])

    return output

  def getLogs(self):
    return self.logs

gainP = 1.046
timeConstantP = 9.998
timeDelayP = 0.403

controller = PidController()
controller.identifyParams(gainP, timeConstantP, timeDelayP, hasDerivative = False)
params = controller.getParams()
print('hi')
