unsigned int i=0 ;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
    i++;
    if(i==1){
    Serial.println("74,77,2,119");
    }
    if(i==2){
    Serial.println("43,85,119,13");
    }
    if(i==3){
    Serial.println("172,18,48,97");
    }
    if(i==4){
    Serial.println("23,3,8,48");
    }
    if(i==5){
    Serial.println("31,32,143,43");
    }
    if(i==6){
    Serial.println("96,34,127,80");
    }
    if(i==7){
    Serial.println("2,52,104,25");
    }
    if(i==8){
    Serial.println("115,24,68,56");
    }
    if(i==9){
    Serial.println("76,40,42,18");
    i = 0;
    }   
    delay(1000);
}
