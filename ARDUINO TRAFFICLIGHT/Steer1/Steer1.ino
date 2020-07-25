#include <Servo.h>

Servo myservo;

int raspicom = A1;
int deg;

const int trig = 9;
const int echo = 8;

long dur;
int dist;

void setup() {
  Serial.begin(9600);
  pinMode(trig, OUTPUT);
  pinMode(echo, INPUT);
  myservo.attach(5);
}

void loop() {
  digitalWrite(trig, LOW);
  delayMicroseconds(2);
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);

  dur = pulseIn(echo, HIGH);
  dist = dur*0.034/2;

  Serial.print("dist :");
  Serial.println(dist);
  
  deg = map(dist, 2, 254, 0, 180);
  Serial.println("| deg: ");
  Serial.println(deg);
  //deg = analogRead(raspicom);
  myservo.write(0);
  delay(10);
}
