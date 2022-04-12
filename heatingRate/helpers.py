def splitData(data):
  datasetA = []
  datasetB = []

  alternatingIndex = 2
  for datum in data:
    if alternatingIndex % 2 == 0:
      datasetA.append(datum)
    else:
      datasetB.append(datum)
    alternatingIndex += 1

  return [datasetA, datasetB]