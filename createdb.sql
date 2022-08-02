CREATE TABLE `Tasks` (
    `CategoryID` VARCHAR(3) NOT NULL,
    `TaskID` VARCHAR(3) NOT NULL,
    `Description` VARCHAR(150),
    `Name` VARCHAR(15),
    `Date` DATE,
    PRIMARY KEY (`CategoryID`,`TaskID`)
);

CREATE TABLE `Category` (
    `UserID` VARCHAR(3) NOT NULL,
    `CategoryID` VARCHAR(3) NOT NULL,
    `CategoryType` VARCHAR(40) NOT NULL,
    PRIMARY KEY (`UserID`,`CategoryID`)
);

CREATE TABLE todo (
	id INTEGER NOT NULL, 
	title VARCHAR(100), 
	complete INT, 
	PRIMARY KEY (id)
);

insert into todo values(1,'make the bed',0);
insert into todo values(2,'groceries shopping',0);


CREATE TABLE "user" (
	"id"	INTEGER NOT NULL,
	"username"	VARCHAR(80),
	"password"	VARCHAR(80),
	PRIMARY KEY("id"),
	UNIQUE("username")
);

insert into "user" values (1,'123','123');
insert into "user" values (2,'anhvuong146','anhvuong1462000');
insert into "user" values (3,'123456','123456');
insert into "user" values (4,'hi','hello');
insert into "user" values (5,'test', 'pass');

CREATE TABLE `Register` (
    `UserID` VARCHAR(3) NOT NULL,
    `Password` VARCHAR(40) NOT NULL,
    `Username` VARCHAR(40) NOT NULL,
    PRIMARY KEY (`UserID`)
);

CREATE TABLE `Login` (
    `Username` VARCHAR(40) NOT NULL,
    `Password` VARCHAR(40) NOT NULL
);

CREATE TABLE survey (
	review_number INTEGER NOT NULL, 
	username VARCHAR(80), 
	review varchar(80), 
	PRIMARY KEY (review_number), 
	FOREIGN KEY(username) REFERENCES "user" ("username")
);

insert into survey values (1,'anhvuong146', 'i loved it');
insert into survey values (2,'hi','Wow amazing web app');
insert into survey values (3,'test', 'Great Website');

CREATE TABLE `Questions` (
    `QuestionID` VARCHAR(3) NOT NULL,
    `question` VARCHAR(40),
    PRIMARY KEY (`QuestionID`)
);

CREATE TABLE `Answers` (
    `AnswerID` VARCHAR(3) NOT NULL,
    `comment` VARCHAR(40),
    `Rate` INT(1) NOT NULL,
    PRIMARY KEY (`AnswerID`)
);
