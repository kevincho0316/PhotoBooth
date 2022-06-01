char cmd;
int key;
int b_key = 0;

void setup() {
  
  // 시리얼 통신 시작 (boadrate: 9600)
  Serial.begin(115200);
  pinMode(13,INPUT);
  pinMode(12,INPUT);
  pinMode(8,INPUT);
  pinMode(7,INPUT);
}

void loop() {

  // 컴퓨터로부터 시리얼 통신이 전송되면, 한줄씩 읽어와서 cmd 변수에 입력
//  if(Serial.available()){
//    digitalWrite(13,HIGH);
    cmd = Serial.read(); 
    if (digitalRead(13) == HIGH){
      key = 1;
    }
    else if(digitalRead(12)== HIGH){
      key = 2;
    } 
    
    else if (digitalRead(8)== HIGH){
      key = 3;
    } 
    
    else if (digitalRead(7)== HIGH){
      key = 4;
    } 
    else{
      key = 0;
      }
    
    Serial.println(key);
    
//    if (b_key != key ){
//      Serial.println(key);
//      b_key = key;
//    }
    delay(400);
}
