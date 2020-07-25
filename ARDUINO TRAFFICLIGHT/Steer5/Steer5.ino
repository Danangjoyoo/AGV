#include <Servo.h>
Servo steerServo;
Servo camServoX;
Servo camServoY;

//deklarasi variabel
int val1,val2,val3,val4,val5,val6,val7,val8;
int bin1,bin2,bin3,bin4,bin5,bin6,bin7,bin8;
int valu1,valu2,valu3,valu4,valu5,valu6,valu7,valu8;
int dir, power, LR, go, degSteer, decimal;
int mid = 90;
int fulp = 255*0.26;

//PIN MOTOR
int in1 = 53;
int in2 = 51;
int in3 = 49;
int in4 = 47;
int velocL = 2;
int velocR = 3;


//PIN COMMAND DARI RASPBERRY
int bit1 = A0;
int bit2 = A1;
int bit3 = A2;
int bit4 = A3;
int bit5 = A4;
int bit6 = A5;
int bit7 = A6;
int LoR = A7;
int MotorP = A9;

//PIN LAMPU
int red = 22;
int LL1 = 24;
int LL2 = 26;
int LL3 = 28;
int LL4 = 30;
int RL1 = 32;
int RL2 = 34;
int RL3 = 36;
int RL4 = 38;

void setup() {
  Serial.begin(9600);
  //=============pin motor
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  pinMode(velocL, OUTPUT);
  pinMode(velocR, OUTPUT);
  //=============pin servo
  steerServo.attach(7);
  steerServo.write(mid);
  camServoX.attach(5);
  camServoX.write(100);
  camServoY.attach(6);
  camServoY.write(80);
  //==============pin lampu
  pinMode(red, OUTPUT);
  pinMode(LL1, OUTPUT);
  pinMode(LL2, OUTPUT);
  pinMode(LL3, OUTPUT);
  pinMode(LL4, OUTPUT);
  pinMode(RL1, OUTPUT);
  pinMode(RL2, OUTPUT);
  pinMode(RL3, OUTPUT);
  pinMode(RL4, OUTPUT);
  digitalWrite(red, HIGH);
  digitalWrite(LL1, LOW);
  digitalWrite(LL2, LOW);
  digitalWrite(LL3, LOW);
  digitalWrite(LL4, LOW);
  digitalWrite(RL1, LOW);
  digitalWrite(RL2, LOW);
  digitalWrite(RL3, LOW);
  digitalWrite(RL4, LOW);
}

void loop() {
  rec_bin();    //baca data binary dari Raspberry
  rec_dir();    //dapet value 'LR'
  rec_power();  //dapet value 'go'
  convertAll(); //dapet value 'bin1-7'
  decimal = bin1+bin2+bin3+bin4+bin5+bin6+bin7;
  //Serial.println(String(bin1)+"|"+String(bin2)+"|"+String(bin3)+"|"+String(bin4)+"|"+String(bin5)+"|"+String(bin6)+"|"+String(bin7));
  Serial.println(decimal);
  degSteer = mid+(LR*decimal);
  if (degSteer<90){           //|
    senkiri();                //|
  }else if (degSteer >= 90){  //|===  LAMPU SEN
    senkanan();               //|
  }                           //|
  Serial.println(String(degSteer)+" ==> " + String(LR*decimal) + " | power: " + String(go));
  steerServo.write(degSteer); //Kendali Steer
  gas();
  delay(50);
  /*if(go==1){
    if (degSteer < 40){
      digitalWrite(velocL, 255*0.90);
      analogWrite(velocR, 255*0.700);
      digitalWrite(in1, LOW);
      digitalWrite(in2, HIGH);
      digitalWrite(in3, LOW);
      digitalWrite(in4, HIGH);
      digitalWrite(red, LOW);
    }
    else if (degSteer >= 40){
      analogWrite(velocL, 255*0.80);
      analogWrite(velocR, 255*0.60);
      digitalWrite(in1, LOW);
      digitalWrite(in2, HIGH);
      digitalWrite(in3, LOW);
      digitalWrite(in4, HIGH);
      digitalWrite(red, LOW);
    }
  }else if(go==0){
    analogWrite(velocL, 0);
    analogWrite(velocR, 0);
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
    digitalWrite(in3, LOW);
    digitalWrite(in4, LOW);
    digitalWrite(red, HIGH);
  }*/
}

//==============================================
////LAMPIRAN FUNGSI-FUNGSI//////==============
//=========================================

//RECEIVED BINARY NUMBER
void rec_bin(){
  val1 = analogRead(bit1);
  val2 = analogRead(bit2);
  val3 = analogRead(bit3);
  val4 = analogRead(bit4);
  val5 = analogRead(bit5);
  val6 = analogRead(bit6);
  val7 = analogRead(bit7);
  dir = analogRead(LoR);
  power = analogRead(MotorP);
  //Serial.println(String(val1)+"|"+String(val2)+"|"+String(val3)+"|"+String(val4)+"|"+String(val5)+"|"+String(val6)+"|"+String(val7));
}

//=================================KONVERSI BILANGAN BINER//
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
  if(val1<600){
    bin1 = 0;
  }else if(val1>600){
    bin1 = 1;}
}
void convert2(){
  if(val2<600){
    bin2 = 0;
  }else if(val2>600){
    bin2 = 2;}
}
void convert3(){
  if(val3<600){
    bin3 = 0;
  }else if(val3>600){
    bin3 = 4;}
}
void convert4(){
  if(val4<600){
    bin4 = 0;
  }else if(val4>600){
    bin4 = 8;}
}
void convert5(){
  if(val5<600){
    bin5 = 0;
  }else if(val5>600){
    bin5 = 16;}
}
void convert6(){
  if(val6<600){
    bin6= 0;
  }else if(val6>600){
    bin6 = 32;}
}
void convert7(){
  if(val7<600){
    bin7 = 0;
  }else if(val7>600){
    bin7 = 64;}
}

//==========================NILAI DERAJAT BELOK
void rec_dir(){
  if(dir<600){
    LR = -1;
  }else if(dir>600){
    LR = 1;
  }
}

//===========================NGEGAS ATAU NGEREM
void rec_power(){
  if(power<600){
    go = 0;
  }else if(power>600){
    go = 1;
  }
}

//==========LAMPU SEN=====
void senkiri(){
  digitalWrite(LL1, HIGH);
  digitalWrite(LL2, HIGH);
  digitalWrite(LL3, HIGH);
  digitalWrite(LL4, HIGH);
  delay(25);
  digitalWrite(LL1, LOW);
  digitalWrite(LL2, LOW);
  digitalWrite(LL3, LOW);
  digitalWrite(LL4, LOW);
  delay(25);
  }
void senkanan(){
  digitalWrite(RL1, HIGH);
  digitalWrite(RL2, HIGH);
  digitalWrite(RL3, HIGH);
  digitalWrite(RL4, HIGH);
  delay(25);
  digitalWrite(RL1, LOW);
  digitalWrite(RL2, LOW);
  digitalWrite(RL3, LOW);
  digitalWrite(RL4, LOW);
  delay(25);
}


void gas(){
  if(go==1){
    if((0 <= decimal) && (decimal <= 30)){
      analogWrite(velocL, int(fulp*0.8));
      analogWrite(velocR, int(fulp*0.8));
      digitalWrite(in1, LOW);
      digitalWrite(in2, HIGH);
      digitalWrite(in3, LOW);
      digitalWrite(in4, HIGH);
      digitalWrite(red, LOW);  
    }else if(30 < decimal){
      analogWrite(velocL, fulp);
      analogWrite(velocR, fulp);
      digitalWrite(in1, LOW);
      digitalWrite(in2, HIGH);
      digitalWrite(in3, LOW);
      digitalWrite(in4, HIGH);
      digitalWrite(red, LOW);
    }
  }else if(go==0){
    analogWrite(velocL, 0);
    analogWrite(velocR, 0);
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
    digitalWrite(in3, LOW);
    digitalWrite(in4, LOW);
    digitalWrite(red, HIGH);
  }
}
