#!/bin/bash

sudo apt-get update
sudo apt-get install -y python3-pip
sudo apt-get install -y ansible

## only pip3 install ansible is negative, which lacks particular ansible configuration(including /usr/bin/ansible is not builded)
## so, first execute sudo apt-get install and then execute pip3 install. And edit shebang of /usr/bin/ansible like python2->python3.
sudo pip3 install ansible
sudo sed -i 's/python2/python3/' /usr/bin/ansible

##move inventory setting
sudo mv hosts /etc/ansible
sudo mv group_vars /etc/ansible

sudo apt-get install -y awscli
pip3 install pywinrm

## done
