import os
import sys
import time
import json
import socket
import hashlib
import urllib.request
from cgitb import enable
from datetime import datetime
from wsgiref.simple_server import server_version

soc = socket.socket()
soc.settimeout(10)

with open("src/userinfo") as userinfo:
    username = userinfo.read().rstrip()

    def getserverip():
        print("Connecting to the Pool IP Address and Port!")
        getpool = False
        while not getpool:
            try:
                serverip = ("https://server.duinocoin.com/getPool")
                poolinfo = json.loads(urllib.request.urlopen(serverip).read())
                global pooladdress, poolport
                pooladdress = poolinfo['ip']
                poolport = poolinfo['port']
                getpool = True
            except:
                print("Connetion Failed!, Retrying...")
                time.sleep(2.3)
                continue

    getserverip()
    while True:
        try:
            soc.connect((str(pooladdress), int(poolport)))
            serverversion = soc.recv(3).decode()

            print("")
            print("------------------------")
            print("IP: ", pooladdress)
            print("Port:", poolport)
            print("Server Version", serverversion)
            print("------------------------")
            print("")
            print("Connected!")
            print("Start Mining...")
            print("")

            while True:
                soc.send(bytes("JOB," + username + ",LOW", encoding="utf8"))
                workjob = soc.recv(1024).decode().rstrip("\n")
                workjob = workjob.split(",")
                difficulty = workjob[2]
                hashingstart = time.time()
                mainhash = hashlib.sha1(str(workjob[0]).encode('ascii'))
                temphash = None

                for result in range(100 * int(difficulty) + 1):
                    temphash = mainhash.copy()
                    temphash.update(str(result).encode('ascii'))
                    duco = temphash.hexdigest()

                    if workjob[1] == duco:
                        hashingstop = time.time()
                        timedifference = hashingstop - hashingstart
                        hashrate =result / timedifference
                        soc.send(bytes(str(result) + "," + str(hashrate) + ",DucoMiner " + "1.0", encoding="utf8"))
                        feedback = soc.recv(1024).decode().rstrip("\n")

                        if feedback == "GOOD":
                            print("[", datetime.today(), "]", "Share", result, "Difficulty", difficulty, "Hashrate", int(hashrate/1000), "kH/s", "(Accepted!)")
                            break
                        elif feedback == "BAD":
                            print("[", datetime.today(), "]", "Share", result, "Difficulty", difficulty, "Hashrate", int(hashrate/1000), "kH/s", "(Rejected!)")
                            break

        except Exception as e:
            print("")
            print("Error occured: " + str(e) + ",restarting in 3s, ")
            print("")
            getserverip()
            time.sleep(3)
            os.execl(sys.executable, sys.executable, *sys.argv)
else:
    exit()
