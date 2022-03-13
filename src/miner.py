import os
import sys
import time
import socket
import hashlib
import multiprocessing
from datetime import datetime

soc = socket.socket()
soc.settimeout(10)

with open("src/userinfo") as userinfo:
    username = userinfo.read().rstrip()
with open("src/thread") as thread:
    thread = thread.read().rstrip()

def getserverip():
    try:
        print("Connecting to the Pool IP Address and Port!")
        pooladdress = "51.158.182.90"
        poolport = 9779
        soc.connect((str(pooladdress), int(poolport)))
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

processes = []
for x in range(int(thread)):
    p = multiprocessing.Process(target=getserverip)
    if __name__ == '__main__':
        p.start()
        processes.append(p)

for p in processes:
    p.join()
