from socket import *
serverPort=12001;
serverSocket=socket(AF_INET, SOCK_STREAM);
serverSocket.bind(('',serverPort));
serverSocket.listen(10);
print "ready!";
while 1:
    connectionSocket, addr=serverSocket.accept();
    sentence=connectionSocket.recv(1024);
    returnSentence=raw_input("return:");
    connectionSocket.send(returnSentence);
    connectionSocket.close();