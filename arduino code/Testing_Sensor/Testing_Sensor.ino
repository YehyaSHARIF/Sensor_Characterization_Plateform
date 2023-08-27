/*
 Ce code est capable de lire le voltage recu par le photodiode à travers de la pin analog A0 chaque 10 ms
*/


void setup() {
  // put your setup code here, to run once:
 Serial.begin(9600);
 

 //Vmax=Amax*(5.0/1023.0);
 //Serial.print("MaxVoltage=");
 //Serial.print(Vmax);
 //Serial.println("V");
 //Serial.print("MaxAnalog=");

 
}

void loop() {
  // put your main code here, to run repeatedly:
  float a = analogRead(A0);
  float voltage=a*(5.0/1023.0);
  int percent=map(a,0,1023,0,100);
   //print out the value you read:
  //Serial.print("Analog Reading:");
  //Serial.print(a);
  //Serial.print(",Voltage=");
  
  Serial.println(voltage);
  //Serial.print("V,Percentage:");
  //Serial.println(percent);
  delay(10);
  //the variation of voltage is between 0.311V and 0.366V we have to use an amplifier
}
