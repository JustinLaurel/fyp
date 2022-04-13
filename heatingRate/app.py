import pandas as pandas
from helpers import splitData
from uc.uc_main import calcUc

file = pandas.ExcelFile(r'C:\Users\Spring\Desktop\heatingRateModel\main.xlsx')
datasetA = pandas.read_excel(file, 'datasetA').values
datasetB = pandas.read_excel(file, 'datasetB').values

print('UC=' + str(calcUc(datasetA, datasetB)))
