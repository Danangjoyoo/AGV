int pinput = A0;

void setup(){
  Serial.begin(9600);
}

void loop(){
  int baca1 = analogRead(pinput);
  Serial.println(baca1);
  delay(500);
}
