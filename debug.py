import time
import socket
import hashlib
import multiprocessing
from datetime import datetime

ip = '51.158.182.90'
port = 9779

username = input("Enter your username: ")
thread = input("Enter how many thread: ")
miner = input("Enter your miner: ")
version = input("Enter your version: ")


def main():
    soc = socket.socket()
    soc.settimeout(10)
    soc.connect((str(ip), int(port)))
    soc.recv(3).decode()

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
                soc.send(bytes(str(result) + "," + str(hashr) + f",{miner} " + f"{version}", encoding="utf8"))
                feedback = soc.recv(1024).decode().rstrip("\n")

                if feedback == "GOOD":
                    print(f"[{datetime.today()}] Share, {result}, Difficulty, {diff}, Hashrate, {int(hashr/1000)}kH/s (Accepted!)")
                    break
                elif feedback == "BAD":
                    print(f"[{datetime.today()}] Share, {result}, Difficulty, {diff}, Hashrate, {int(hashr/1000)}kH/s (Rejected!)")
                    break
processes = []

for x in range(int(thread)):
    p = multiprocessing.Process(target=main)
    if __name__ == '__main__':
        p.start()
        processes.append(p)


for p in processes:
    p.join()
