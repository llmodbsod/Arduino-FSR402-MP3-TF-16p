#include "mp3tf16p.h"

#define LED_PIN 13
#define FSR_PIN A0          // FSR connected to A0 (FSR + 10kΩ to GND)

// MP3 Player

MP3Player mp3(10, 11);

// Detection thresholds
int pressThreshold = 900;   // adjust this based on your FSR readings
int releaseThreshold = 200; // for hysteresis
bool isPressed = false;     // state tracking

void setup(void)
{
  Serial.begin(9600);
  pinMode(LED_PIN, OUTPUT);
  pinMode(FSR_PIN, INPUT);

  mp3.initialize();
  mp3.player.volume(25);  // set volume 0–30

  Serial.println("System ready — waiting for pressure...");
}

void loop(void)
{
  int fsrValue = analogRead(FSR_PIN);

  // --- Debugging output ---
  Serial.print("FSR value: ");
  Serial.println(fsrValue);

  // --- Pressure detection logic ---
  if (!isPressed && fsrValue > pressThreshold)
  {
    isPressed = true;

    Serial.println("Pressure detected! Playing sound...");

    digitalWrite(LED_PIN, HIGH);
    mp3.playTrackNumber(1, 25, false); // play track 1 at volume 25 (non-blocking)
  }
  else if (isPressed && fsrValue < releaseThreshold)
  {
    // Pressure released
    isPressed = false;
    digitalWrite(LED_PIN, LOW);
  }

  delay(100); // small debounce
}
