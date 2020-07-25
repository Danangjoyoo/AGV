int ledR = 2;
int ledY = 3;
int ledG = 4;
int motor = 5;

void setup() {
  Serial.begin(9600);
  pinMode(ledR, OUTPUT);
  pinMode(ledY, OUTPUT);
  pinMode(ledG, OUTPUT);
  pinMode(motor, OUTPUT);
  digitalWrite(ledR, LOW);
  digitalWrite(ledY, LOW);
  digitalWrite(ledG, LOW);
}

void loop() {
  digitalWrite(ledR, HIGH);
  //analogWrite(motor, 255);
  /*delay(3000);
  digitalWrite(ledG, LOW);
  digitalWrite(ledR, HIGH);
  delay(3000);
  
  /*delay(1000);
  //digitalWrite(ledY, HIGH);
  digitalWrite(ledG, HIGH);
  delay(5000);
  digitalWrite(ledG, LOW);
  delay(1000);
  
 /* digitalWrite(ledR, HIGH);
  digitalWrite(ledY, LOW);
  digitalWrite(ledG, LOW);
  delay(1000);
  digitalWrite(ledR, LOW);
  digitalWrite(ledY, HIGH);
  digitalWrite(ledG, LOW);
  delay(1000);
  digitalWrite(ledR, LOW);
  digitalWrite(ledY, LOW);
  digitalWrite(ledG, HIGH);
  delay(1000);
*/
}
