sudo apt update
sudo apt install default-jdk
sudo useradd -r -m -U -d /opt/tomcat -s /bin/false tomcat

wget https://dlcdn.apache.org/tomcat/tomcat-9/v9.0.63/bin/apache-tomcat-9.0.63.tar.gz -P /tmp
sudo tar xf /tmp/apache-tomcat-9.0.63.tar.gz -C /opt/tomcat
sudo ln -s /opt/tomcat/apache-tomcat-9.0.63 /opt/tomcat/latest
sudo chown -RH tomcat: /opt/tomcat/latest
sudo sh -c 'chmod +x /opt/tomcat/latest/bin/*.sh'
