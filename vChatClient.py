from socket import *
serverName='118.89.229.68';
serverPort=12001;
while 1:
    clientSocket = socket(AF_INET, SOCK_STREAM);
    clientSocket.connect((serverName, serverPort));
    sentence=raw_input('Input:');
    clientSocket.send(sentence);
    relay=clientSocket.recv(1024);
    print relay;
    clientSocket.close();
    raw_input("press enter to continue");

