


create database vchat;
create table userData
(
	`userName` varchar(100),
    `CP` varchar(100),
    `pwd` varchar(100)
    
);

create table chatLogs
(
	id INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
	`contents` varchar(1000),
    `userName` varchar(100),
    `serverTime` varchar(100)
    
)AUTO_INCREMENT = 1;