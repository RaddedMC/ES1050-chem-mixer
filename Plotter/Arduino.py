## WesternU ES1050 Fall 2021 -- S24T3 Chemical mixer plotter code -- Arduino.py
## James N, Maya A, Ola O, Griffin M, Harp T
## Code by James

# This class will keep track of the connected Arduino and grab nicely formatted strings from its serial console.

import serial

class Arduino:
    serialConnection = None

    # Constructor
    def __init__(self, port, baudrate, timeout):
        self.serialConnection = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)

    # Read a line from the serial connection -- strip away any extra crap and make sure the line isn't blank
    def readline(self):
        linenotblank = False
        while not linenotblank:
            ## Read a line
            line = self.serialConnection.readline()

            ## If the line is blank, break out of the loop
            if line:
                linenotblank = True
        
        line = (str(line)[2:])[:-5]

        return line