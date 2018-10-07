#include <Servo.h>

Servo myservo1; //left
Servo myservo2; //right

void setup() {
  myservo1.attach(9);
  myservo2.attach(10);
  myservo1.writeMicroseconds(1500);
  myservo2.writeMicroseconds(1500);
}

void loop() {

  if(Serial.available() > 0){
    unsigned char cmd = Serial.read();
    //process the byte
    
    //get intensity
    unsigned char intensity = cmd & 0b00001111;
    //map it from 0 to 100
    intensity = (map, 0, 15, 0, 100);

    if((cmd >> 6) | 0x00 == 0x00){
      //drive forward
      myservo1.writeMicroseconds(1500 + (500 * (intensity / 100.0)));
      myservo2.writeMicroseconds(1500 + (500 * (intensity / 100.0)));
    }

    if((cmd >> 6) & 0x01 == 0x01){
      //drive right
      myservo1.writeMicroseconds(1500 + (500 * (intensity / 100.0)));
      myservo2.writeMicroseconds(1500 - (500 * (intensity / 100.0)));
    }

    if((cmd >> 6) & 0x10 == 0x10){
      //drive left
      myservo1.writeMicroseconds(1500 - (500 * (intensity / 100.0)));
      myservo2.writeMicroseconds(1500 + (500 * (intensity / 100.0)));
    }
  }


}
