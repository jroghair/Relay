#include <Servo.h>

Servo myservo1; //left
Servo myservo2; //right
double intensity = 15;
double turnIntensity = 10;

void setup() {
  Serial.begin(115200);
  myservo1.attach(9);
  myservo2.attach(10);
  //myservo1.writeMicroseconds(1500);
  //myservo2.writeMicroseconds(1500);
}

void loop() {

  if(Serial.available() > 0){
    char command = Serial.read();
    command &= 0xFF;
    
    if(command == 'f'){
      myservo1.writeMicroseconds(1500 - (intensity / 50.0 * 500.0));
      myservo2.writeMicroseconds(1500 + (intensity / 50.0 * 500.0));
    }else if(command == 'r'){
      myservo1.writeMicroseconds(1500 + (turnIntensity / 50.0 * 500.0));
      myservo2.writeMicroseconds(1500 + (turnIntensity / 50.0 * 500.0));
    }else if(command == 'l'){
      myservo1.writeMicroseconds(1500 - (turnIntensity / 50.0 * 500.0));
      myservo2.writeMicroseconds(1500 - (turnIntensity / 50.0 * 500.0));
    }else if(command == 's'){
      myservo1.writeMicroseconds(1500);
      myservo2.writeMicroseconds(1500);
    }

  }

}
