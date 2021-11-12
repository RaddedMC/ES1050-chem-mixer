## WesternU ES1050 Fall 2021 -- S24T3 Chemical mixer plotter code -- Parser.py
## James N, Maya A, Ola O, Griffin M, Harp T
## Code by James

# This function will parse a single plot point from the connected arduino and return a Plot.

from Plot import Plot
from Arduino import Arduino
import re

# TODO: make arduino output a different colour

def parsePlot(arduino):
    ## Grab the string block

    # block order: time, pressure, expectedpressure, *expectedpressurerate, *errorrange, valvestate
    stringblock = [arduino.readline() for s in range(0,6)]

    ## Print the string block
    for s in stringblock:
        print(s)

    ## Parse the string block into a Plot
    #/ regex from https://stackoverflow.com/questions/4703390/how-to-extract-a-floating-number-from-a-string

    # time
    plotTime = findTheFloat(stringblock[0])

    # pressure
    plotPressure = findTheFloat(stringblock[1])

    # valve state
    plotValveState = "OPEN" in stringblock[5] # this is why I use python :D

    #~ statics
    if not Plot.staticsDefined():
        print("Grabbing static values...")
        Plot.expectedPressureRate = findTheFloat(stringblock[3])
        Plot.errorRange = findTheFloat(stringblock[4])
        print("Expected pressure rate is " + str(Plot.expectedPressureRate) + " PSI/MIN")
        print("Error range is +- " + str(Plot.errorRange) + " PSI")

    ## Return a plot
    plot = Plot(plotPressure, plotTime, plotValveState)
    print("Plot collected: " + str(plot))
    return plot

def findTheFloat(s):
    return float(float(re.findall(r"[-+]?\d*\.\d+|\d+", s)[0]))