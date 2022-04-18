from jitcdde import t, y, jitcdde
import numpy as np

# the constants in the equation
b = 1/50
d = 1/75
a = 0.8
G = 10**(-2)
tau = 0.5

# the equation
f = [    
  b * (y(1) - y(0)) * y(0) / y(1) - d * y(0, t-tau),
  G * (a*y(1) - y(0)) * y(0) / y(1)
]
y_one = y(1)

# initialising the integrator
DDE = jitcdde(f)

# enter initial conditions
N0 = 0.1
No0 = 10
DDE.add_past_point(-1.0, [N0,No0], [0.0, 0.0])
DDE.add_past_point( 0.0, [N0,No0], [0.0, 0.0])

# short pre-integration to take care of discontinuities
DDE.step_on_discontinuities()

# create timescale
times = np.linspace(1, 1000, 100)

# integrating
data = []
for time in times:
    data.append( DDE.integrate(time) )

print('hello')
