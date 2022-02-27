#!/bin/sh
cd
rm -rf ducominer
rm -rf DucoMiner
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip git
git clone https://github.com/lolenseu/DucoMiner.git
cd DucoMiner
chmod +x start.sh && ./start.sh
chmod +x start.sh && ./update.sh
