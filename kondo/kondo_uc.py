import pandas
from uc.uc_kondo import calcUc

file = pandas.ExcelFile(r'C:\Users\Spring\Desktop\heatingRateModel\kondo.xlsx')
datasetA = pandas.read_excel(file, 'datasetA').values
datasetB = pandas.read_excel(file, 'datasetB').values

print(
  calcUc(datasetA, datasetB)
)