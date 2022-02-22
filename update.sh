#!/bin/sh
cd
rm -rf DucoMiner
sudo apt update && sudo apt upgrade -y
apt install python3 python3-pip git
git clone https://github.com/lolenseu/DucoMiner.git
cd DucoMiner

