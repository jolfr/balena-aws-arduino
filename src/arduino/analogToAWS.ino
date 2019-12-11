/* 
 *  analogToAWS.ino
 *  Arduino code for Balena-AWS-Arduino project
 *  By Jack Carroll
*/
#define SensorPin A0  // analog sensor pin
float sensorValue = 0; 
int period = 5000;  // time between measurements
unsigned long time_now = 0; // time at last measurement
void setup() { 
 Serial.begin(9600);  // serial port opened at 9600 baud
} 
void loop() { 
 if(millis() > time_now + period){ 
    time_now = millis();
    for (int i = 0; i <= 100; i++) // take 100 measurements and then average to reduce noise
     { 
       sensorValue = sensorValue + analogRead(SensorPin); 
       delay(1); 
     } 
     sensorValue = sensorValue/100.0; 
     Serial.println(sensorValue); // print to serial output
 }
}