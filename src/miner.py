import os
import sys
import time
import json
import socket
import hashlib
import urllib.request
import multiprocessing
from cgitb import enable
from datetime import datetime
from wsgiref.simple_server import server_version

soc = socket.socket()
soc.settimeout(10)

with open("src/userinfo") as userinfo:
    username = userinfo.read().rstrip()
with open("src/thread") as thread:
    thread = thread.read().rstrip()
processes = []
    
def getserverip():
    print("Connecting to the Pool IP Address and Port!")
    getpool = False
    while not getpool:
        try:
            serverip = ("https://server.duinocoin.com/getPool")
            poolinfo = json.loads(urllib.request.urlopen(serverip).read())
            global pooladdress, poolport, poolserver, poolname, poolconnection
            pooladdress = poolinfo['ip']
            poolport = poolinfo['port']
            poolserver = poolinfo['server']
            poolname = poolinfo['name']
            poolconnection = poolinfo['success']
            getpool = True
        except:
            print("Connetion Failed!, Retrying...")
            time.sleep(2.3)
            continue
            
    while True:
    try:
        soc.connect((str(51.158.182.90), int(9779)))
        soc.recv(3).decode()
        print("")
        print("Connected!")
        print("Start Mining...")
        print("")

        while True:
            soc.send(bytes("JOB," + username + ",LOW", encoding="utf8"))
            work = soc.recv(1024).decode().rstrip("\n")
            work = work.split(",")
            diff = work[2]
            start = time.time()
            mainhash = hashlib.sha1(str(work[0]).encode('ascii'))
            temphash = None

            for result in range(100 * int(diff) + 1):
                temphash = mainhash.copy()
                temphash.update(str(result).encode('ascii'))
                duco = temphash.hexdigest()

                if work[1] == duco:
                    stop = time.time()
                    timediff = stop - start
                    hashr = result / timediff
                    soc.send(bytes(str(result) + "," + str(hashr) + ",DucoMiner " + "1.1", encoding="utf8"))
                    feedback = soc.recv(1024).decode().rstrip("\n")

                    if feedback == "GOOD":
                        print(f"[{datetime.today()}] Share, {result}, Difficulty, {diff}, Hashrate, {int(hashr/1000)}kH/s (Accepted!)")
                        break
                    elif feedback == "BAD":
                        print(f"[{datetime.today()}] Share, {result}, Difficulty, {diff}, Hashrate, {int(hashr/1000)}kH/s (Rejected!)")
                        break

    except Exception as e:
        print("")
        print("Error occured: " + str(e) + ",restarting in 3s, ")
        print("")
        getserverip()
        time.sleep(3)
        os.execl(sys.executable, sys.executable, *sys.argv)


for x in range(thread):
    p = multiprocessing.Process(target=getserverip)
    if __name__ == '__main__':
        p.start()
        processes.append(p)
        
for p in processes:
    p.join()
