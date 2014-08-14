#! /bin/sh

sudo apt-get install -y python3
sudo apt-get install -y python-pip
sudo apt-get install -y python3-dev
sudo apt-get install -y libpq-dev postgresql


## INSTALL ELASTICSEARCH

# update apt
sudo apt-get update
# install java
sudo apt-get install openjdk-7-jre-headless -y
# install elasticsearch

wget https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.3.1.deb
dpkg -i elasticsearch-1.3.1.deb


sudo service elasticsearch start


sudo apt-get install -y git
git clone https://github.com/nyddle/toster.git
