/*
 Ce code capable de lire le voltage recu par le photodiode et la distance lue par le laser sensor
 sous la forme [volt;distance]
*/
//les variables necessaire pour lire le voltage de la photodiode
float value;
float vout;

//les variables necessaires pour lire la distance de laser sensor
//----------------------------------------------------------------
float SumA0 = 0;
float OffsetA0 = 0;
float WindowSize = 20;
float WindowSizeBegin = 200;
float WindowSizeBackup;
float NStartSkipFrames = 100;
float SkipFramesCounter = 0;
int Counter = 0;
bool Beginning = true;
//----------------------------------------------------------------
float OpticalSensorReading()
{
  value = analogRead(A0);     //Read the value                                           //Just like we did earlier
  vout = (5.0 / 1023.0) * value;         // Calculates the voltage
 
  return value,vout;
}
//----------------------------------------------------------------
void setup() {
  // put your setup code here, to run once:
Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  float AZero = analogRead(A1);
  SumA0 += AZero;

  Counter++;

  if (Counter >= WindowSize)
  {
    float MeanA0 = SumA0 / WindowSize;
    float DistInMM = (MeanA0 / 1023) * 70 - 35 + 0.18+0.7+0.35; // Convert to mm and adjust with a small factor to match readings from display on the backside of the device
   
    value,vout = OpticalSensorReading();
  
    Serial.print(vout,2);
    Serial.print(";");
    Serial.println(DistInMM,1);
    delay(200);
    Counter = 0;
    SumA0 = 0;
    Serial.flush();
    
  }

  delay(10);
}
