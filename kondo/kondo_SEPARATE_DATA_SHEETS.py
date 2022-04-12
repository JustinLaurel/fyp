import pandas as pandas
from uc.uc_kondo import calcUc

file = pandas.ExcelFile(r'C:\Users\Spring\Desktop\heatingRateModel\kondo.xlsx')
datasetA = pandas.read_excel(file, 'x3_SMALL_A').values
datasetB = pandas.read_excel(file, 'x3_SMALL_B').values

print('UC for kondo=' + str(calcUc(datasetA, datasetB)))
