import pandas as pandas
from helpers import splitData
from uc.uc_main import calcUc

HEATING_RATE = 0
CURRENT_TEMP = 1
DIESEL_FLOW = 2
NITROGEN_FLOW = 3
BIOMASS_MASS = 4
CHAR_MASS = 5

file = pandas.ExcelFile(r'C:\Users\Spring\Desktop\heatingRateModel\m2_temp.xlsx')
lowData = pandas.read_excel(file, 'LOW').values
highData = pandas.read_excel(file, 'HIGH').values

[lowDatasetA, lowDatasetB] = splitData(lowData)
[highDatasetA, highDatasetB] = splitData(highData)

print('UC for LOW=' + str(calcUc(lowDatasetA, lowDatasetB)))
print('UC for HIGH=' + str(calcUc(highDatasetA, highDatasetB)))