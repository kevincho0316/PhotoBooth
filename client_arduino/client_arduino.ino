int pq_v = true;
int pw_v = true;
int pe_v = true;
int pt_v = true;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(12, INPUT);
  pinMode(11, INPUT);
  pinMode(10, INPUT);
  pinMode(7, INPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
  
  int q_v = digitalRead(7);
  int w_v = digitalRead(12);
  int e_v = digitalRead(11);
  int t_v = digitalRead(10);

  
  if(pq_v == false && q_v==true){
    Serial.println("q");
    }
  else if(pw_v == false && w_v==true){
    Serial.println("w");
    }
  else if(pe_v == false && e_v==true){
    Serial.println("e");
    }
  
  else if(pt_v == false && t_v==true){
    Serial.println("t");
    }
  else{
    Serial.println("");
    }
  pq_v = q_v;

  pt_v = t_v;
  pe_v = e_v;
  pw_v = w_v;
  
//  Serial.println(readV);

  delay(100);
  
}
