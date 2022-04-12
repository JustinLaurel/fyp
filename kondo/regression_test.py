inputOutputData = [
  [1, 3, 1, 1, 11.1],
  [1, 5, 2, 1, 6.5],
  [1, 1, 3, 5, 10.2],
  [1, 3, 4, 5, 6],
  [1, 5, 5, 1, 5.2],
  [5, 1, 4, 1, 19],
  [5, 3, 3, 5, 14.2],
  [5, 5, 2, 5, 14.4],
  [5, 1, 1, 1, 27.4],
  [5, 3, 2, 1, 15.4],
  [1, 5, 3, 5, 5.7],
  [1, 1, 4, 5, 9.8],
  [1, 3, 5, 1, 5.9],
  [1, 5, 4, 1, 5.4],
  [1, 1, 3, 5, 10.2],
  [5, 3, 2, 5, 15.4],
  [5, 5, 1, 1, 19.7],
  [5, 1, 2, 1, 21.1],
  [5, 3, 3, 5, 14.2],
  [5, 5, 4, 5, 12.7]
]

X1_INDEX = 0
X2_INDEX = 1
X3_INDEX = 2
X4_INDEX = 3
OUTPUT_INDEX = 4

def calc(x1, x2, x3, x4):
  fireStrength_1 = 0
  fireStrength_2 = 0
  if (x3 > 1.1) & (x3 < 2.2): fireStrength_1 = (-0.9091 * x3) + 2
  elif (x3 <= 1.1):           fireStrength_1 = 1
  else:                       fireStrength_1 = 0

  if (x3 > 1.1) & (x3 < 2.2): fireStrength_2 = (0.9091 * x3) - 1
  elif (x3 >= 2.2):           fireStrength_2 = 1
  else:                       fireStrength_2 = 0

  return (
    fireStrength_1 * (3.13*x1 - 1.91*x2 + 13.6*x3) + \
    fireStrength_2 * (8.92 + 1.84*x1 - 1.32*x2 + 0.14*x3)
  )

for datum in inputOutputData:
  datum[OUTPUT_INDEX] = calc(
    datum[X1_INDEX],
    datum[X2_INDEX],
    datum[X3_INDEX],
    datum[X4_INDEX]
  )
  print(datum)