#! /bin/sh

sudo apt-get update

sudo apt-get install -y python3 python-dev python-pip
sudo apt-get install -y libpq-dev postgresql postgresql-contrib

## INSTALL ELASTICSEARCH

# install java
sudo apt-get install openjdk-7-jre-headless -y

wget https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.3.2.deb
#wget https://github.com/nyddle/toster/blob/adavydov_vagrant/misc/elasticsearch-1.3.1.deb
dpkg -i elasticsearch-1.3.1.deb


sudo service elasticsearch start


sudo apt-get install -y git
git clone https://github.com/nyddle/toster.git

su - postgres psql -c 'create database toster;'

#TODO: we are mot actually using virtual env right now 
pip install virtualenv
mkdir  envs
virtualenv envs/toster --distribute --python python3.4
cd toster
source ../envs/toster/bin/activate
pip install -r requirements.txt

