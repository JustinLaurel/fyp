**Code structure is a complete mess

1. Go to heatingRate/heatingRateWriter.py and run the file
2. An excel file named 'main.xlsx' will be created in heatingRate folder once the script finishes running. This is the input-output data
    - Input-output data can have its ranges changed by changing the linspace values
3. Go to heatingRateConsequents.py
4. Change the path parameter on the pandas.ExcelFile() function call to the path to the main.xlsx excel file that heatingRateWriter.py created. Use an absolute path
5. Run heatingRateConsequents.py. Once it finishes running, the consequent parameters in datatype: [y-intercept, diesel flow rate (kg/s), current reactor temperature (K)] is stored in the consequentParams variable near the end of file, and will be printed out
6. Alternatively, run heatingRateConsequents.py in debugging mode, and put a breakpoint at print statement at the end to see the the a clearer view on the value of consequentParams
7. consequentParams contain the y-intercept, diesel flow rate(kg/s) and current reactor temperature (K) parameters for every single rule in the fuzzy model, using the multiple least squares method
8. 25 rules were used in the model
9. Logic for generation of fuzzy rules is found in the same heatingRateConsequents.py file
