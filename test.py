sensorTemp = 299.5782563976733
innerTempWithTimeDelay = 314.7809878995382
innerTemp = 331.6888141186551

value = (-sensorTemp + innerTempWithTimeDelay) / (0.0004*innerTemp**0.8725)
print(value)