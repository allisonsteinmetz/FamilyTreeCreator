CREATE TABLE Account (
  email VARCHAR(100) NOT NULL,
  username VARCHAR(80),
  PRIMARY KEY(email)
);
  
CREATE TABLE Treelist (
  email VARCHAR(100) NOT NULL,
  treeID INT NOT NULL,
  treeName VARCHAR(100),
  URL VARCHAR(100),
  PRIMARY KEY(treeID),
  FOREIGN KEY(email) REFERENCES Account(email)
);


CREATE TABLE morris_1 (
  personID INT NOT NULL AUTO_INCREMENT,
  motherID INT,
  fatherID INT,
  name VARCHAR(80),
  gender CHAR(1),
  birthday DATE,
  PRIMARY KEY(personID)
);



/////////

INSERT INTO Person(name, gender, birthday) 
VALUES
('Jacob Morris', 'M', '1960-00-00'),
('Olivia Nash', 'F', '1960-00-00'),
('Alexander Dawson', 'M', '1960-00-00'),
('Sophia Foster', 'F', '1960-00-00');

INSERT INTO Person(name, motherID, fatherID, gender, birthday)
VALUES 
('Thomas Morris', 2, 1 ,'M', '1980-00-00'),
('Isabella Dawson', 4, 3, 
