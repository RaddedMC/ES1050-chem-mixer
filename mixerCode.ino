// WesternU ES1050 Fall 2021 -- S24T3 Chemical mixer code
// James N, Maya A, Ola O, Griffin M, Harp T
// Code by James

// TODO: Baseline pressure
// TODO: Live graphing

#define sensorPin A5
#define valvePin 8

// ADJUST THESE TO CHANGE REACTION CONTROL BEHAVIOUR//
#define pressureRate 4
// in psi/min

#define pressureRange 0.5
// in psi

#define baselinePointsCount 5

double baseline = 0;
double timeoffset = -4.0;

// Adjust this to change what happens when you turn on and off the valve
void setValveState(bool state) {
  if (state) {
    digitalWrite(valvePin, HIGH);
    digitalWrite(LED_BUILTIN, HIGH);
  } else {
    digitalWrite(valvePin, LOW);
    digitalWrite(LED_BUILTIN, LOW);
  }
}

// Grabs the average ambient pressure 
double calibrateBaseline() {
  double pressureBaseline = 0;
  for (int i = 0; i < baselinePointsCount; i++) {
    double pressure = getPressure(false);
    pressureBaseline += pressure;
    Serial.print("Pressure: "); Serial.println(pressure);
  }
  pressureBaseline /= baselinePointsCount;
  Serial.print("Baseline pressure is "); Serial.print(pressureBaseline); Serial.println(" PSI.");
  return pressureBaseline;
}

void setup() {
  Serial.begin(9600);
  Serial.println("Hemlo am wake");
  Serial.println("Defining pins...");

  // Sensor pin
  pinMode(sensorPin, INPUT);

  // Valve pin
  pinMode(valvePin, OUTPUT);

  // Valve test
  Serial.println("Testing valve.. should be ON!");
  setValveState(true);
  delay(1000);
  Serial.println("OFF!");
  setValveState(false);
  delay(1000);

  // Tell user what the current maths are
  Serial.print("Expected pressure rate is ");
  Serial.print(pressureRate);
  Serial.println(" psi per minute.");
  Serial.print("With an error of +- ");
  Serial.print(pressureRange);
  Serial.println(" psi.");
  delay(2000);

  // Calibrate baseline
  baseline = calibrateBaseline();
  
  Serial.println("~~~ BEGIN!!! ~~~");
}

// Uses millis() to get what the current pressure should be
double getIntendedPressure() {
  // 4 psi per minute = 4/60 psi per second
  double pressureRateSeconds = pressureRate / 60.0;
  double time = (millis()+(timeoffset*1000.0)) / 1000.0; // convert to seconds
  // linear growth -- y = mx+b
  double intendedPressure = pressureRateSeconds * time;
  return intendedPressure;
}

// Grabs and returns the current pressure value
double getPressure(boolean pressureAdjusted) {
  // 0.5 volts = 0 psi
  // 4.5 volts = 30 psi
  int digitalValue = analogRead(sensorPin);
  double volts = 5.0 * (digitalValue / 255.0);
  double pressure = 30.0 * (volts / 4.0);
  return pressureAdjusted ? pressure - baseline : pressure;
}

// Should we open the valve?
bool valveState(double pressure, double intendedPressure) {
  // What should the pressure range be?
  double intendedPressureHigh = intendedPressure + pressureRange;

  // If the pressure is greater than the maximum...
  // We should open the valve!
  return (pressure >= intendedPressureHigh);
}

void loop() {
  Serial.println("------------------------------");
    Serial.print("TIME:                    ");
  Serial.println(millis()/1000.0);

  // Check current pressure
  double pressure = getPressure(true);
    Serial.print("PRESSURE:               ");
  Serial.print(pressure);
  Serial.println(" PSI");

  // Check intended pressure
  double intendedPressure = getIntendedPressure();
    Serial.print("EXPECTED PRESSURE:      ");
  Serial.print(intendedPressure);
  Serial.println(" PSI");

  // Extra outputs for fanciness
    Serial.print("PRESSURE RATE: ");
  Serial.print(pressureRate);
  Serial.println(" PSI / MIN");
    Serial.print("ERROR RANGE: +-         ");
  Serial.print(pressureRange);
  Serial.println(" PSI");

  // Open valve?
  bool valveOpen = valveState(pressure, intendedPressure);
  setValveState(valveOpen);
  if (valveOpen) {
    Serial.println("VALVE IS:               OPEN");
  } else {
    Serial.println("VALVE IS:             CLOSED");
  }
}
