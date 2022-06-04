 git clone https://github.com/kevincho0316/PhotoBooth
 apt install python3-pip
 pip3 install --upgrade pip
 pip3 install -r requirements.txt


wget https://dlcdn.apache.org/tomcat/tomcat-9/v9.0.63/bin/apache-tomcat-9.0.63.tar.gz -P /tmp
sudo tar xf /tmp/apache-tomcat-9.0.63.tar.gz -C /opt/tomcat
sudo ln -s /opt/tomcat/apache-tomcat-9.0.63 /opt/tomcat/latest
sudo chown -RH tomcat: /opt/tomcat/latest
sudo sh -c 'chmod +x /opt/tomcat/latest/bin/*.sh'

<Context path="/p" docBase="/home/hellochs/PhotoBooth/product" reloadable="false" allowLinking="true"></Context>

<Context path="" docBase="/user/local/" reloadable="false" allowLinking="false"></Context>





https://jjeongil.tistory.com/1351

