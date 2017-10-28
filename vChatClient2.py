#coding:utf-8
from socket import *
import time, threading
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

serverName = '127.0.0.1';
sendPort = 12001;
receivePort = 12002;
checkPort = 12003;
userName = "";
key = "";
pwd = "";

def sendThread():
    while 1:
        sentence = raw_input();
        sentence += "_";
        sentence += userName;
        sentence += "_";
        sentence += key;
        sentence += "_";
        sentence += pwd;
        clientSocket = socket(AF_INET, SOCK_STREAM);
        clientSocket.connect((serverName, sendPort));
        clientSocket.send(sentence);
        checker = clientSocket.recv(2048);
        if (checker=="fuck"):
            print("\n!!!Don't try to cheat!!!\n");

        clientSocket.close();

def receiveThread():
    while 1:
        time.sleep(0.5);
        monitorSocket = socket(AF_INET, SOCK_STREAM);
        monitorSocket.connect((serverName, receivePort));
        monitorSocket.send(key+"_"+userName+"_"+pwd);
        relay = monitorSocket.recv(2048);
        if relay:
            print ">>>"+relay;
        monitorSocket.close();


while 1:
    # 0->succuss, 1->wrong pwd, 2-> wrong room keyword
    userName = raw_input("Your name: ");
    key = raw_input("Chat room keyword: ");
    pwd = raw_input("Your own keyword: ");
    clientSocket = socket(AF_INET, SOCK_STREAM);
    clientSocket.connect((serverName, checkPort));
    clientSocket.send(key+"_"+userName+"_"+pwd);
    relay = clientSocket.recv(2048);
    clientSocket.close();
    if relay == "0":
        print (">>>Welcome to vChat!\n");
        t1 = threading.Thread(target=sendThread);
        t2 = threading.Thread(target=receiveThread);
        t1.start();
        t2.start();
        t1.join();
        t2.join();
        break;

    elif relay == "1":
        print ("! Wrong pwd");

    else:
        print ("! Wrong room keyword");



raw_input("Press any key to continue...");