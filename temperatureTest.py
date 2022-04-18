
dT_dt = (
  (
  43999997.7*mDiesel - 1751.9*currentTemp*mDiesel + 1750*mDiesel*initialTemp - 2.326*mDiesel - 3.76*mDiesel*currentTemp**2 + 3.76*mDiesel*currentTemp*initialTemp + 1.8972*mDiesel*initialTemp
  ) / (1440*mSolid + 175.8 + 1061884.6/currentTemp)
)