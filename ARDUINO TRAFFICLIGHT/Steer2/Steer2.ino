#include <Servo.h>

Servo myservo;

//int raspicom = 5;
int bit1 = 8;
int bit2 = 9;
int bit3 = 10;
int bit4 = 11;
//int deg;

void setup() {
  Serial.begin(9600);
  pinMode(bit1, OUTPUT);
  pinMode(bit2, OUTPUT);
  pinMode(bit3, OUTPUT);
  pinMode(bit4, OUTPUT);
  digitalWrite(bit1, LOW);
  digitalWrite(bit2, LOW);
  digitalWrite(bit3, LOW);
  digitalWrite(bit4, LOW);
  //pinMode(raspicom, OUTPUT);
  //myservo.attach(5);
}

void loop() {
  r12();
  delay(2000);
  r7();
  delay(2000);
  
  //Serial.print("| deg: ");
  //Serial.println(deg);
  //for(int i = 0; i<=180; i+=1){
    //deg = map(i, 0, 180, 0 ,255);
    //analogWrite(raspicom, 150);
    //Serial.println(deg);
    //i += 45;
    //delay(1000);
  //deg = analogRead(raspicom);
  //myservo.write(0);
  delay(10);
}

void r12(){
  digitalWrite(bit1, HIGH);
  digitalWrite(bit2, HIGH);
  digitalWrite(bit3, HIGH);
  digitalWrite(bit4, LOW);
}

void r7(){
  digitalWrite(bit1, LOW);
  digitalWrite(bit2, LOW);
  digitalWrite(bit3, HIGH);
  digitalWrite(bit4, LOW);
}
