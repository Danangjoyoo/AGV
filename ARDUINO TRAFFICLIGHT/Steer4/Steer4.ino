#include <Servo.h>
Servo myservo;

//deklarasi variabel
int val1,val2,val3,val4,val5,val6,val7,val8;
int bin1,bin2,bin3,bin4,bin5,bin6,bin7,bin8;
int valu1,valu2,valu3,valu4,valu5,valu6,valu7,valu8;
int dir, power, LR, go, degSteer, decimal;
int mid = 90;
int red = 0;

//PIN MOTOR
int V_right = A0;
int in1 = A1;
int in2 = A2;
int V_left = A3;
int in3 = A4;
int in4 = A5;

//PIN COMMAND DARI RASPBERRY
int bit1 = 13;
int bit2 = 12;
int bit3 = 11;
int bit4 = 10;
int bit5 = 9;
int bit6 = 8;
int bit7 = 7;
int LoR = 6;
int MotorP = 5;

void setup() {
  Serial.begin(9600);
  pinMode(red, OUTPUT);
  //pin motor
  pinMode(V_right, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(V_left, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  myservo.attach(3);
  myservo.write(mid);
  digitalWrite(red, HIGH);
}

void loop() {
  rec_bin();
  rec_dir();
  rec_power();
  convertAll();
  decimal = bin1+bin2+bin3+bin4+bin5+bin6+bin7;
  Serial.println(String(bin1)+"|"+String(bin2)+"|"+String(bin3)+"|"+String(bin4)+"|"+String(bin5)+"|"+String(bin6)+"|"+String(bin7));
  //Serial.println(decimal);
  degSteer = mid+(decimal*LR);
  Serial.print(degSteer);
  myservo.write(degSteer);
  gas();
}

//==============================================
////LAMPIRAN FUNGSI-FUNGSI//////==============
//=========================================

//RECEIVED BINARY NUMBER
void rec_bin(){
  val1 = digitalRead(bit1);
  val2 = digitalRead(bit2);
  val3 = digitalRead(bit3);
  val4 = digitalRead(bit4);
  val5 = digitalRead(bit5);
  val6 = digitalRead(bit6);
  val7 = digitalRead(bit7);
  dir = digitalRead(LoR);
  power = digitalRead(MotorP);
}

//KONVERSI BILANGAN BINER//
void convertAll(){
  convert1();
  convert2();
  convert3();
  convert4();
  convert5();
  convert6();
  convert7();
}
void convert1(){
  if(val1==LOW){
    bin1 = 0;
  }else if(val1==HIGH){
    bin1 = 1;}
}
void convert2(){
  if(val2==LOW){
    bin2 = 0;
  }else if(val2==HIGH){
    bin2 = 2;}
}
void convert3(){
  if(val3==LOW){
    bin3 = 0;
  }else if(val3==HIGH){
    bin3 = 4;}
}
void convert4(){
  if(val4==LOW){
    bin4 = 0;
  }else if(val4==HIGH){
    bin4 = 8;}
}
void convert5(){
  if(val5==LOW){
    bin5 = 0;
  }else if(val5==HIGH){
    bin5 = 16;}
}
void convert6(){
  if(val6==LOW){
    bin6= 0;
  }else if(val6==HIGH){
    bin6 = 32;}
}
void convert7(){
  if(val7==LOW){
    bin7 = 0;
  }else if(val7==HIGH){
    bin7 = 64;}
}

//NILAI DERAJAT BELOK
void rec_dir(){
  if(dir==LOW){
    LR = -1;
  }else if(dir==HIGH){
    LR = 1;
  }
}

//NGEGAS ATAU NGEREM
void rec_power(){
  if(power==LOW){
    go = 0;
  }else if(power==HIGH){
    go = 1;
  }
}

void gas(){
  if(go==1){
    analogWrite(V_right, 255);
    analogWrite(V_left, 255);
    digitalWrite(red, LOW);
  }else if(go==0){
    analogWrite(V_right, 0);
    analogWrite(V_left, 0);
    digitalWrite(red, HIGH);
  }
}
