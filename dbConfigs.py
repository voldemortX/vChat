import pymysql

#configurations for database vChat
vChatConfigs = {'host':'127.0.0.1',
                'port':3306,
                'user':'root',
                'password':"********",
                'db':"vchat",
                'charset':'utf8',
                'cursorclass': pymysql.cursors.DictCursor};


