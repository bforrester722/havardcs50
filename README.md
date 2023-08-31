# havardcs50

Harvard's CS50 Web Programming with Python and JavaScript

CREATE TABLE flights(
id INTEGER PRIMARY KEY AUTOINCREMENT,
origin TEXT NOT NULL,
destination TEXT NOT NULL,
duration INTEGER NOT NULL
);
INSERT INTO flights (origin,destination ,duration) VALUES( 'Shanghai', 'Paris' , 760);
INSERT INTO flights (origin,destination ,duration) VALUES( 'Istanbul', 'Tokyo' , 700);
INSERT INTO flights (origin,destination ,duration) VALUES( 'New York', 'Paris' , 435);
INSERT INTO flights (origin,destination ,duration) VALUES( 'Moscow', 'Paris' , 245);
INSERT INTO flights (origin,destination ,duration) VALUES( 'Lima', 'New York' , 455);

UPDATE flights SET duration = 430 WHERE origin = 'New York' AND destination = 'London';
