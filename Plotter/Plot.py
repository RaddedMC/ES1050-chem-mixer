## WesternU ES1050 Fall 2021 -- S24T3 Chemical mixer plotter code -- Plot.py
## James N, Maya A, Ola O, Griffin M, Harp T
## Code by James

# Plot classes will be used to keep track of points on the graph and what data they contain.
# Comparable to a block of output from the Arduino console.

class Plot:
    # STATIC
    errorRange = 0
    expectedPressureRate = 0

    # INSTANCE
    currentPressure = 0
    time = 0
    valveState = False

    # Constructor
    def __init__(self, currentPressure:currentPressure, time:time, valveState:valveState):
        # TODO: these may not be necessary
        self.currentPressure = currentPressure
        self.time = time
        self.valveState = valveState

    # Checks if static fields are defined so that they aren't defined twice
    def staticsDefined():
        return (Plot.errorRange and Plot.expectedPressureRate)

    # Describes the plot
    def __str__(self):
        return (str(self.time)+ "s: Valve " + ("ON" if self.valveState else "OFF") + " at " + str(self.currentPressure) + " PSI")