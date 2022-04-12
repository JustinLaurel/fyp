import pandas as pandas
from uc.uc_main import calcUc

SHEET1 = 'datasetA'
SHEET2 = 'datasetB'
HEATING_RATE = 0
CURRENT_TEMP = 1
DIESEL_FLOW = 2
NITROGEN_FLOW = 3
BIOMASS_MASS = 4
CHAR_MASS = 5

file = pandas.ExcelFile(r'C:\Users\Spring\Desktop\heatingRateModel\main.xlsx')
sheet1 = pandas.read_excel(file, SHEET1)
sheet2 = pandas.read_excel(file, SHEET2)

datasetA = sheet1.values
datasetB = sheet2.values

print('UC=' + str(calcUc(datasetA, datasetB)))