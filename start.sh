#!/bin/sh
clear
echo ""
echo "------------------------"
echo "|                      |"
echo "|      DuinoMiner      |"
echo "|         V1.0         |"
echo "|                      |"
echo "------------------------"
echo ""
echo "Username:"
read uservar
echo $uservar > src/userinfo
echo ""
python3 src/miner.py
