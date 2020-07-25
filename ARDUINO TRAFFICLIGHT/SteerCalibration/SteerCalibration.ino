#include <Servo.h>
Servo steer;



void setup() {
  steer.attach(7);
  
}

void loop() {
  steer.write(40);
  delay(500);
  steer.write(130);
  delay(500);
}
