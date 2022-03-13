#!/bin/sh
clear
echo ""
echo "------------------------"
echo "|                      |"
echo "|      DuinoMiner      |"
echo "|         V1.1         |"
echo "|                      |"
echo "------------------------"
echo ""
echo "Username:"
read uservar
echo "Thread:"
read threadvar
echo $uservar > src/userinfo
echo $threadvar > src/thread
echo ""
python3 src/miner.py
