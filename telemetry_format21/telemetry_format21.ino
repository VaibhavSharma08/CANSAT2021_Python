unsigned int i=0 ;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
    i++;
    Serial.print("4800,1234567,");
    Serial.print(i);
    Serial.print(",12,0,0,0,");
    if(i==1){
    Serial.print("74,77,2,119");
    }
    if(i==2){
    Serial.print("43,85,119,13");
    }
    if(i==3){
    Serial.print("172,18,48,97");
    }
    if(i==4){
    Serial.print("23,3,8,48");
    }
    if(i==5){
    Serial.print("31,32,143,43");
    }
    if(i==6){
    Serial.print("96,34,127,80");
    }
    if(i==7){
    Serial.print("2,52,104,25");
    }
    if(i==8){
    Serial.print("115,24,68,56");
    }
    if(i==9){
    Serial.print("76,40,42,18");
    i = 0;
    }   
    Serial.println("0,0,0,0,0,0,0,0,0");
    delay(1000);
}
