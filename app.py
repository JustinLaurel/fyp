from scipy.integrate import odeint
import numpy as numpy
import matplotlib.pyplot as plot
from math import exp

def odes(
  x, 
  t,
  heatingRate = 300, # K/s
  initialTemp = 293, # K
):
  # constants
  a1 = 2.8e19
  a2 = 3.28e14
  a3 = 1.3e10

  a4 = 2.1e16
  a5 = 8.75e15
  a6 = 2.6e11

  a7 = 9.6e8
  a8 = 1.5e9
  a9 = 7.7e6

  a10 = 4.25e6

  #Cellulose
  K1 = -29153.89
  K2 = -23633.41
  K3 = -18100.91

  #Hemicellulose
  K4 = -22454.75
  K5 = -24343.02
  K6 = -17523.60

  #Lignin
  K7 = -12941.25
  K8 = -17295.09
  K9 = -13398.28

  #Tar
  K10 = -12989.36

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

  yc = 0.35
  yh = 0.60
  yl = 0.75

  #True densities
  pb = 380      #biomass
  pc = 350      #char
  pg = 1.2506   #gas

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



  return [
    dm1_dt, # Cellulose
    dm2_dt, # Hemicellulose
    dm3_dt, # Lignin
    dm4_dt, # Active Cellulose
    dm5_dt, # Active Hemicellulose
    dm6_dt, # Active Lignin
    dm7_dt, # Tar
    dm8_dt, # Gas
    dm9_dt  # Char
  ]

# initial conditions
x0 = [  #Composition @ t=0, kg
  42, #Cellulose
  32, #Hemicellulose
  26, #Lignin
  0,  #Active cellulose
  0,  #Active hemicellulose
  0,  #Active lignin
  0,  #Tar
  0,  #Gas
  0,  #Char
]

# constants
timeRangeSeconds = 4
heatingRate = 200
initialTemp = 293

# time vector (time window)
t = numpy.linspace(0, timeRangeSeconds, 500)
x = odeint(odes, x0, t, (heatingRate,))

m1 = x[:, 0]
m2 = x[:, 1]
m3 = x[:, 2]
m4 = x[:, 3]
m5 = x[:, 4]
m6 = x[:, 5]
m7 = x[:, 6]
m8 = x[:, 7]
m9 = x[:, 8]

def annot_max(x, y, ax=None):
  xmax = x[numpy.argmax(y)]
  ymax = y.max()
  text = "max yield: {:.2f}kg @ {:.3f}s".format(ymax, xmax)
  if not ax:
    ax = plot.gca()
  bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
  arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=60")
  kw = dict(
    xycoords='data',
    textcoords="axes fraction",
    arrowprops=arrowprops,
    bbox=bbox_props,
    ha="right",
    va="top"
  )
  ax.annotate(text, xy=(xmax, ymax), xytext=(0.94,0.96), **kw)

ax = plot.subplots()

# plot the results
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
plot.plot(t, m8, label="gas")
plot.plot(t, m9, label="char")
plot.legend()

annot_max(t, m7)
# annot_max(t, m9)

plot.ylim(0, 100)
plot.show()

