int ki1 = 53;
int ki2 = 51;
int ka1 = 49;
int ka2 = 47;
int v1  = 2;
int v2  = 3;

void setup() {
  Serial.begin(9600);
  pinMode(ki1, OUTPUT);
  pinMode(ki2, OUTPUT);
  pinMode(ka1, OUTPUT);
  pinMode(ka2, OUTPUT);
  pinMode(v1, OUTPUT);
  pinMode(v2, OUTPUT);
}

void loop() {
  analogWrite(v1, 255);
  analogWrite(v2, 255);
  digitalWrite(ki1, LOW);
  digitalWrite(ki2, HIGH);
  digitalWrite(ka1, LOW);
  digitalWrite(ka2, HIGH);
  delay(1000);
  analogWrite(v1, 200);
  analogWrite(v2, 200);
  digitalWrite(ki1, LOW);
  digitalWrite(ki2, HIGH);
  digitalWrite(ka1, LOW);
  digitalWrite(ka2, HIGH);
  delay(1000);
  analogWrite(v1, 150);
  analogWrite(v2, 150);
  digitalWrite(ki1, LOW);
  digitalWrite(ki2, HIGH);
  digitalWrite(ka1, LOW);
  digitalWrite(ka2, HIGH);
  delay(1000);
  analogWrite(v1, 100);
  analogWrite(v2, 100);
  digitalWrite(ki1, LOW);
  digitalWrite(ki2, HIGH);
  digitalWrite(ka1, LOW);
  digitalWrite(ka2, HIGH);
  delay(1000);
  analogWrite(v1, 50);
  analogWrite(v2, 50);
  digitalWrite(ki1, LOW);
  digitalWrite(ki2, HIGH);
  digitalWrite(ka1, LOW);
  digitalWrite(ka2, HIGH);
  delay(1000);
  analogWrite(v1, 0);
  analogWrite(v2, 0);
  digitalWrite(ki1, LOW);
  digitalWrite(ki2, HIGH);
  digitalWrite(ka1, LOW);
  digitalWrite(ka2, HIGH);
  delay(1000);
}
