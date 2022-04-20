from random import randint

import matplotlib.pyplot as plot
import numpy

def addModelDataHeaders(excelSheet):
  excelSheet.write(0, 0, 'Tar yield (kg)')
  excelSheet.write(0, 1, 'Tungsten heating rate (K/s)')
  excelSheet.write(0, 2, 'Initial biomass mass (kg)')



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

def trimArray(array, desiredLength):
  arrayLength = len(array)
  for i in range(arrayLength):
    if (len(array) > desiredLength):
      randomNumber = round(randint(0, len(array) - 1))
      del array[randomNumber]
  return array

def getAverage(valuesArray):
  total = 0
  if len(valuesArray) == 0: return 0
  for value in valuesArray:
    total += value

  return total / len(valuesArray)

def addTarHeaders(excelSheet):
  excelSheet.write(0, 0, 'Final tar yield (kg)')
  excelSheet.write(0, 1, 'Actual residence time (s)')
  excelSheet.write(0, 2, 'Heating rate (K/s)')
  excelSheet.write(0, 3, 'Nitrogen Flowrate (kg/s)')
  excelSheet.write(0, 4, 'Diesel flowrate (kg/s)')
  return excelSheet

def addHeatingRateHeaders(excelSheet):
  excelSheet.write(0, 0, 'Heating Rate (K/s)')
  excelSheet.write(0, 1, 'Current T (K)')
  excelSheet.write(0, 2, 'Diesel Flowrate (kg/s)')
  excelSheet.write(0, 3, 'Nitrogen Flowrate (kg/s)')
  excelSheet.write(0, 4, 'Biomass mass (kg)')
  excelSheet.write(0, 5, 'Char mass (kg)')
  return excelSheet

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

def sortByTime(list):
  def takeTime(element):
    return element['time']

  return sorted(list, key=takeTime)

def getLastTimeChangeData(historyList, current_t):
  sorted = sortByTime(historyList)
  for history in reversed(sorted):
    if history['time'] < current_t:
      return history

  return None