#!/bin/sh
clear
echo ""
echo "------------------------"
echo "|                      |"
echo "|      DuinoMiner      |"
echo "|         V1.2         |"
echo "|                      |"
echo "------------------------"
echo ""
echo "Username:"
read uservar
echo "Key:"
read keuvar
echo $uservar > src/userinfo
echo $key > src/key
echo ""
python3 src/miner.py
