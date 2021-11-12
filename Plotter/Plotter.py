## WesternU ES1050 Fall 2021 -- S24T3 Chemical mixer plotter code -- Plotter.py
## James N, Maya A, Ola O, Griffin M, Harp T
## Code by James

# The plotter file will be used to collect data and plot points coming from the Arduino

### PRESETS ###
# Serial settings
comport = "COM8"
baudrate = 9600
timeout=0.1

### IMPORTS ###

import time
import Plot
from Arduino import Arduino
from Plot import Plot
import Parser
import matplotlib.pyplot as pyplot
from matplotlib.animation import FuncAnimation


## THE MAIN METHOD
def main():
    print("ES1050 S24T3 -- Mixer plotter")
    print("by JamesN // RaddedMC\n")
    
    print("Opening serial console...")
    arduino = Arduino(port=comport, baudrate=baudrate, timeout=timeout)

    print("Serial console opened! Setting up the graph and waiting for data...")

    # Now that we know the Arduino's working, let's set up our graph
    plots = []
    ani = FuncAnimation(pyplot.gcf(), animate, fargs=(plots, arduino))


    pyplot.show()

    # TODO: save data as CSV?

    print("Graph closed! Exiting...")
    exit(0)

        
## Animate is called by PyPlot to collect any new data
# Got a lot of help from https://saralgyaan.com/posts/python-realtime-plotting-matplotlib-tutorial-chapter-9-35-36/
def animate(i, plots, arduino):
    waitForNewPlot(arduino)
    print("Plot found! Starting data parsing...")

    plots.append(Parser.parsePlot(arduino))

    print("Plot collected! Adding to graph...")

    pyplot.cla()
    pyplot.plot([plot.time for plot in plots], [plot.currentPressure for plot in plots]) # Current pressure
    pyplot.plot([plot.time for plot in plots], [[(plot.time/60.0)*Plot.expectedPressureRate] for plot in plots]) # Expected pressure


# This way the plotter doesn't accidentally pick up garbage data
def waitForNewPlot(arduino):
    print("Waiting for new plot...")
    plotfound = False
    while not plotfound:
        currentline = arduino.readline()
        if currentline[0:1] == "-":
            plotfound = True
        print(currentline)



# blah blah blah python things
if __name__ == "__main__":
    main()