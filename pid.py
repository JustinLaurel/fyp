class PidController():
  def __init__(self, gainP = None, timeConstantP = None, timeDelayP = None):
    if (timeDelayP is not None):
      self.generateParams(gainP, timeConstantP, timeDelayP)
    
    self.outputLogs = []
    self.feedbackLogs = []
    self.errorLogs = []
    self.integralErrorLogs = []
    self.derivativeFeedbackLogs = []

    self.proportionalLogs = []
    self.integralLogs = []
    self.differentialLogs = []
    self.setpointLogs = []

  def getParams(self):
    if self.gain is None: raise Exception('PID controller parameters are not defined')
    return [
      self.gain,
      self.timeConstant,
      self.integralConstant
    ]

  def generateParams(self, gainP, timeConstantP, timeDelayP):
    self.timeConstant = max(0.1*timeConstantP, 0.8*timeDelayP)
    self.gain = (0.586/gainP) * ((timeDelayP / timeConstantP) ** -0.916)
    self.integralConstant = timeConstantP / (1.03 - 0.165*(timeDelayP / timeConstantP))

    return [self.gain, self.timeConstant, self.integralConstant]

  def calculateOutput(self, error, t):
    proportional = self.gain * error
    integral = 

gainP = 1.046
timeConstantP = 9.998
timeDelayP = 0.403

controller = PidController()
controller.generateParams(gainP, timeConstantP, timeDelayP)
gain, timeConstant, integralConstant = controller.getParams()

print('gain: ' + str(gain))
print('timeConstant: ' + str(timeConstant))
print('integralConstant: ' + str(integralConstant))