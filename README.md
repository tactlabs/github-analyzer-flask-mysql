# github-analyzer-flask-mysql
GitHub Analyzer

[![HitCount](http://hits.dwyl.io/teamtact/https://github.com/teamtact/github-analyzer-flask-mysql.svg)](http://hits.dwyl.io/teamtact/https://github.com/teamtact/github-analyzer-flask-mysql)

```
CREATE USER test@localhost IDENTIFIED BY 'test';
GRANT ALL PRIVILEGES ON test.* TO test@localhost;

CREATE TABLE CITY(
	ID INT PRIMARY KEY AUTO_INCREMENT,
	NAME VARCHAR(50),
	STATE VARCHAR(50),
	COUNTRY VARCHAR(50)
);

INSERT INTO CITY (NAME, STATE, COUNTRY) VALUES ('San Francisco', 'CA', 'US');
INSERT INTO CITY (NAME, STATE, COUNTRY) VALUES ('Chennai', 'TA', 'India');
INSERT INTO CITY (NAME, STATE, COUNTRY) VALUES ('Madurai', 'TA', 'India');
INSERT INTO CITY (NAME, STATE, COUNTRY) VALUES ('Bengalore', 'KA', 'India');
```
