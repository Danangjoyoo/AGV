#include <Servo.h>

Servo myservo;

//int raspicom = A1;
int bit1 = A4;
int bit2 = A3;
int bit3 = A2;
int bit4 = A1;
int deg, val1, val2, val3, val4;
int vall1, vall2,vall3,vall4;
int bin1,bin2,bin3,bin4;

void setup() {
  Serial.begin(9600);
  //pinMode(raspicom, INPUT);
  //myservo.attach(6);
}

void loop() {
  val1 = analogRead(bit1);
  val_1();
  convert1();
  val2 = analogRead(bit2);
  val_2();
  convert2();
  val3 = analogRead(bit3);
  val_3();
  convert3();
  val4 = analogRead(bit4);
  val_4();
  convert4();
  Serial.print(" | BinaryNum :");
  Serial.println(String(vall1)+(" ")+String(vall2)+(" ")+String(vall3)+(" ")+String(vall4));
  Serial.print(" | DecimalNum: ");
  Serial.print(bin1+bin2+bin3+bin4);
  delay(100);
  
  /*for(deg=0;deg<180;deg++){
  deg = analogRead(raspicom);
  Serial.print("deg: ");
  Serial.println(deg);
  deg = map(deg, 0, 1023, 0, 180);
  Serial.print("map :");
  Serial.println(deg);
  myservo.write(deg);
  //deg += 1;*/
  //delay(1000);
}

void val_1(){
  if (val1<500){
    vall1 = 0;
  }else{
    vall1 = 1;}
}

void val_2(){
  if (val2<500){
    vall2 = 0;
  }else{
    vall2 = 1;}
}

void val_3(){
  if (val3<500){
    vall3 = 0;
  }else{
    vall3 = 1;}
}

void val_4(){
  if (val4<500){
    vall4 = 0;
  }else{
    vall4 = 1;}
}
/////////////FUNGSI KONVERSI BINARY NUMBER///////
void convert1(){
  if(vall1 == 0){
    bin1 = 0;
  }else if(vall1 == 1){
    bin1 = 1;
  }
}
void convert2(){
  if(vall2 == 0){
    bin2 = 0;
  }else if(vall2 == 1){
    bin2 = 2;
  }
}
void convert3(){
  if(vall3 == 0){
    bin3 = 0;
  }else if(vall3 == 1){
    bin3 = 4;
  }
}
void convert4(){
  if(vall4 == 0){
    bin4 = 0;
  }else if(vall4 == 1){
    bin4 = 8;
  }
}
