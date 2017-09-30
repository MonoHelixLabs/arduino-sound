/****************************************
Sound level for multiple microphone amplifiers
and a button
****************************************/

// mics
const int sampleWindow = 6; // Sample window width in mS (50 mS = 20Hz)
unsigned int sample;

// button
const int buttonPin = 2;     // the number of the pushbutton pin
int buttonState = 0;         // variable for reading the pushbutton status
int newButtonState = 0;
bool active = true;

void setup() 
{
   pinMode(buttonPin, INPUT);   
   Serial.begin(9600);
}


void readMics() {
  
  for(int i=0; i<5; i++) {
       unsigned long startMillis= millis();  // Start of sample window
       unsigned int peakToPeak = 0;   // peak-to-peak level
    
       unsigned int signalMax = 0;
       unsigned int signalMin = 1024;
       // collect data for sampleWindow mS
       while (millis() - startMillis < sampleWindow)
       {
          sample = analogRead(i);
          if (sample < 1024)  // toss out spurious readings
          {
             if (sample > signalMax)
             {
                signalMax = sample;  // save just the max levels
             }
             else if (sample < signalMin)
             {
                signalMin = sample;  // save just the min levels
             }
          }
       }
       peakToPeak = signalMax - signalMin;  // max - min = peak-peak amplitude
       double volts = (peakToPeak * 5.0) / 1024;  // convert to volts
       Serial.print(volts);
       Serial.print(" ");
     }
     Serial.println();
}

void loop() 
{
   newButtonState = digitalRead(buttonPin);
   
   if (newButtonState != buttonState) {
    if (newButtonState == HIGH) {
      // time to change things
      active = !active;
      if (active == false) {
          Serial.println("save");
      }
    }
    buttonState = newButtonState;
   }

   if (active == true) {
        readMics();
        }
      
}
