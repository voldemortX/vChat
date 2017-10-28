#coding:utf-8
from socket import *
import threading,time
import pymysql
from dbConfigs import vChatConfigs
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

sendPort = 12001;
receivePort = 12002;
checkPort = 12003;
#set room key
key = "runningseagull";


def sendThread():
    #content, userName, key, pwd
    print ("ready-send!");
    sendSocket=socket(AF_INET, SOCK_STREAM);
    sendSocket.bind(('',sendPort));
    sendSocket.listen(100);
    while 1:
        conn = pymysql.connect(**vChatConfigs);
        cursor = conn.cursor();
        sendSocketT, addr=sendSocket.accept();
        sentence=sendSocketT.recv(2048);
        myResults=sentence.split("_");
        #check user in DB
        query = "SELECT * FROM userData WHERE userName = %s AND `pwd` = %s";
        data = (myResults[1], myResults[3]);
        cursor.execute(query, data);
        sqlResults = cursor.fetchone();

        if myResults[2] != key or (not sqlResults):
            sendSocketT.send("fuck");#fucker check

        else:
            myResults[2]=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()));
            query = "INSERT INTO `chatLogs` (`contents`,`userName`, `serverTime`) VALUES (%s,%s,%s) ";
            data = (myResults[0],myResults[1],myResults[2]);
            cursor.execute(query, data);
            cursor.close();
            conn.commit();
            conn.close();


        sendSocketT.close();


def receiveThread():
    #key, userName, pwd
    print ("ready-receive!");
    receiveSocket = socket(AF_INET, SOCK_STREAM);
    receiveSocket.bind(('',receivePort));
    receiveSocket.listen(100);
    while 1:
        receiveSocketT, addr=receiveSocket.accept();
        sentence=receiveSocketT.recv(2048);
        myResults=sentence.split("_");
        if myResults[0] != key:
            try:
                receiveSocketT.send("fuck");#fucker check
            except:
                receiveSocketT.close();

        else:
            conn = pymysql.connect(**vChatConfigs);
            cursor = conn.cursor();
            #check user in DB
            query = "SELECT * FROM userData WHERE userName = %s AND `pwd` = %s";
            data = (myResults[1],myResults[2]);
            cursor.execute(query, data);
            sqlResults=cursor.fetchone();
            if sqlResults:
                p = sqlResults['CP'];# current position
                query = "SELECT * FROM chatLogs WHERE id > %s";#find new posts
                data = (p);
                cursor.execute(query, data);
                sqlResults=cursor.fetchall();
                tot = "";
                for sqlResult in sqlResults:
                    tot = tot + sqlResult['serverTime'] + " " + sqlResult['userName'] + ": " + sqlResult['contents'] + "\n";

                newP = str(int(p)+len(sqlResults));#update position
                query = "UPDATE userData SET `CP` = %s WHERE `userName` = %s";
                data=(newP,myResults[1]);
                cursor.execute(query,data);

                cursor.close();
                conn.commit();
                conn.close();
                try:
                    receiveSocketT.send(tot);
                except:
                    receiveSocketT.close();

        receiveSocketT.close();


def checkThread():
    #0->succuss, 1->wrong pwd, 2-> wrong room keyword
    #key, userName, pwd
    print ("ready-check!");
    checkSocket=socket(AF_INET, SOCK_STREAM);
    checkSocket.bind(('',checkPort));
    checkSocket.listen(100);
    while 1:
        checkSocketT, addr=checkSocket.accept();
        sentence=checkSocketT.recv(2048);
        status="0";
        myResults=sentence.split("_");
        if myResults[0] != key:
            status = "2";#fucker check

        else:
            conn = pymysql.connect(**vChatConfigs);
            cursor = conn.cursor();
            query = "SELECT * FROM chatLogs ORDER BY `id` DESC";
            cursor.execute(query);
            sqlResults = cursor.fetchone();
            currentPos = sqlResults['id'];#interesting
            if currentPos == "1":
                currentPos = "2";

            #set user
            query = "SELECT * FROM userData WHERE userName = %s";
            data = (myResults[1]);
            cursor.execute(query, data);
            sqlResults = cursor.fetchone();

            if sqlResults:
                #user already exist
                if sqlResults['pwd'] == myResults[2]:
                    query = "UPDATE userData SET `CP` = %s WHERE `userName` = %s";
                    data = (currentPos,myResults[1]);
                    cursor.execute(query, data);
                else:
                    status = "1";

            else:
            #new user register then login automatically
                query = "INSERT INTO userData (`userName`,`CP`,`pwd`) VALUES(%s,%s,%s)";
                data = (myResults[1],currentPos,myResults[2]);
                cursor.execute(query, data);

            if (status == "0"):
                # login message
                nowTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()));
                query = "INSERT INTO `chatLogs` (`contents`,`userName`, `serverTime`) VALUES (%s,%s,%s) ";
                data = ("---"+myResults[1]+" JUST JOINED THIS ROOM AT "+ nowTime + "---", " ", " ");
                cursor.execute(query, data);

            cursor.close();
            conn.commit();
            conn.close();
            checkSocketT.send(status);


        checkSocketT.close();


print ("ready!");
#asnyc
t1 = threading.Thread(target=sendThread);
t2 = threading.Thread(target=receiveThread);
t3 = threading.Thread(target=checkThread);
t1.start();
t2.start();
t3.start();
t1.join();
t2.join();
t3.join();
