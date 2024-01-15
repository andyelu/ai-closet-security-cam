int sensorValue;
int sensorLow = 1023;
int sensorHigh = 0;
const int ledPin = 13;
unsigned long previousMillis = 0; // will store last time the light was updated
const long interval = 1000; // interval at which to check light (milliseconds)

void setup() {
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, HIGH);
  Serial.begin(9600);
  
  while (millis() < 5000) {
    sensorValue = analogRead(A0);
    if (sensorValue < sensorLow) {
      sensorLow = sensorValue;
    }
    if (sensorValue > sensorHigh) {
      sensorHigh = sensorValue;
    }
  }
  digitalWrite(ledPin, LOW);
}

void loop() {
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= interval) {
    // save the last time the light level was checked
    previousMillis = currentMillis;

    // Check the light level
    sensorValue = analogRead(A0);
    int pitch = map(sensorValue, sensorLow, sensorHigh, 50, 4000);
    tone(8, pitch, 20);

    if(sensorValue > 1) {
      Serial.println(sensorValue);
    }
  }
}
