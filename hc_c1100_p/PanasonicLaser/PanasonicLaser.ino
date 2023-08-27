// Digitizing and converting the values of the Panasonic HG-C1100-P
// This particular sensor meassures +-35mm from an offset distance of 100mm 
// The analog output represents -35mm to +35mm between 0 and 5V 

void setup()
{
  Serial.begin(115200);
  //Serial.println("Reading MPX4250 DP values");
  delay(100);

  pinMode(A0, INPUT);  
}

float SumA0 = 0;
float OffsetA0 = 0;
float WindowSize = 20;
float WindowSizeBegin = 200;
float WindowSizeBackup;
float NStartSkipFrames = 100;
float SkipFramesCounter = 0;
int Counter = 0;
bool Beginning = true;


void loop()
{
  float AZero = analogRead(A0);

  //  if (SkipFramesCounter <=NStartSkipFrames)
  //  {
  //    SkipFramesCounter += 1;
  //    Serial.print(0);
  //    Serial.print(',');
  //    Serial.println(0);
  //    return; // should go for next loop
  //  }

  SumA0 += AZero;

  Counter++;

  if (Counter >= WindowSize)
  {
    float MeanA0 = SumA0 / WindowSize;    
    float DistInMM = (MeanA0/1023)*70 - 35 + 0.18; // Convert to mm and adjust with a small factor to match readings from display on the backside of the device

    //Serial.print(MeanA0);
    //Serial.print(",");
    Serial.println(DistInMM);
    
    Counter = 0;
    SumA0 = 0;    
  }
  
}
