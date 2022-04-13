import pandas as pandas
from ucResidenceTime import calcUc

file = pandas.ExcelFile(r'C:\Users\Spring\Desktop\plantModel\main.xlsx')
datasetA = pandas.read_excel(file, 'datasetA').values
datasetB = pandas.read_excel(file, 'datasetB').values

print('UC=' + str(calcUc(datasetA, datasetB)))
