import os, sys, time, json, socket, hashlib
from urllib import request
from datetime import datetime


soc = socket.socket()
soc.settimeout(None)

appversion = 'v1.2'
print(f"\n--------------------\n|                  |\n|    DuinoMiner    |\n|       {appversion}       |\n|                  |\n--------------------\n")
#username = str(input("Username: "))

class status:
    sok = '[ok!]' #ok status
    ser = '[er!]' #error status
    sgd = '[gd!]' #good status
    sbd = '[bd!]' #bad status
    sac = '(accepted!)' #aceepted status
    sre = '(rejected!)' #rejected status

def getserver():
    print("Getting Server...")
    try:
        serverip = str('https://server.duinocoin.com/getPool')
        poolinfo = json.loads(request.urlopen(serverip).read())
        print(f"Getting Server {status.sok}, Success.")
    except:
        print(f"Getting Server {status.ser}, Retrying...")
        time.sleep(2.3)
        getserver()

    #print(poolinfo) for debuging
    pooladdress = poolinfo['ip']
    poolport = poolinfo['port']
    poolserver = poolinfo['server']
    poolname = poolinfo['name']
    poolconnection = poolinfo['success']
    return pooladdress, poolport, poolserver, poolname, poolconnection    

def results(result, diff, hashr, sstatus):
    print(f"[{datetime.today()}] Share, {result}, Difficulty, {diff}, Hashrate, {int(hashr/1000)}kH/s {sstatus}")
    
def infoserver(server):
    print(f"\n--------------------\nServer Name: {server[3]}\nIP: {server[0]}\nPort: {server[1]}\n--------------------\n")

def main():
    server = getserver()
    print("Connecting Server...")
    try:
        soc.connect((str(server[0]), int(server[1])))
        print(f"Connecting Server {status.sok}, Success.")
    except:
        print(f"Connecting Server {status.ser}, Retrying...")
        time.sleep(2.3)
        main()

main()