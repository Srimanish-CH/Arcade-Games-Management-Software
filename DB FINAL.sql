-- Creating the database
DROP DATABASE IF EXISTS arcade_games_management_system;
CREATE DATABASE arcade_games_management_system;
USE arcade_games_management_system;

-- Creating the GAMECATEGORIES table
DROP TABLE IF EXISTS GAMECATEGORIES;
CREATE TABLE IF NOT EXISTS GAMECATEGORIES (
  CategoryID INT NOT NULL AUTO_INCREMENT,
  Genre VARCHAR(255) NOT NULL,
  MachinesCount INT DEFAULT '0',
  GamesCount INT DEFAULT '0',
  PRIMARY KEY (CategoryID)
) AUTO_INCREMENT=100 DEFAULT CHARSET=utf8mb4;

INSERT INTO GAMECATEGORIES (Genre) VALUES 
('RACING'),
('FIRST PERSON SHOOTER'),
('SPORTS'),
('MULTI-PLAYER'),
('STRATEGY');


-- Creating the GAMES table
DROP TABLE IF EXISTS GAMES;
CREATE TABLE GAMES (
  GameID INT NOT NULL AUTO_INCREMENT,
  GameCategory INT NOT NULL,
  Name VARCHAR(25) NOT NULL,
  credits_required INT NOT NULL,
  gain_tokens INT NOT NULL,
  PRIMARY KEY (GameID),
  KEY GameCategory (GameCategory),
  CONSTRAINT games_ibfk_1 FOREIGN KEY (GameCategory) REFERENCES GAMECATEGORIES (CategoryID)
) AUTO_INCREMENT=200 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Inserting data into the GAMES table
INSERT INTO games (GameCategory, Name, credits_required, gain_tokens) VALUES
(100, 'Formula 1 Racing', 500, 80),
(100, 'Street Racing Challenge', 300, 50),
(100, 'Off-Road Rally', 450, 70);

-- First Person Shooter category
INSERT INTO games (GameCategory, Name, credits_required, gain_tokens) VALUES
(101, 'Call of Duty', 550, 90),
(101, 'Counter-Strike', 400, 65),
(101, 'Battlefield V', 600, 100);

-- Sports category
INSERT INTO games (GameCategory, Name, credits_required, gain_tokens) VALUES
(102, 'FIFA 22', 350, 60),
(102, 'NBA 2K22', 300, 50),
(102, 'Madden NFL 22', 400, 70);

-- Multi-Player category
INSERT INTO games (GameCategory, Name, credits_required, gain_tokens) VALUES
(103, 'Among Us', 200, 30),
(103, 'Fortnite', 450, 75),
(103, 'Apex Legends', 500, 80);

-- Strategy category
INSERT INTO games (GameCategory, Name, credits_required, gain_tokens) VALUES
(104, 'Civilization VI', 550, 90),
(104, 'Starcraft II', 500, 80),
(104, 'Age of Empires IV', 600, 100);
UNLOCK TABLES;

-- Creating the machines table
DROP TABLE IF EXISTS machines;
CREATE TABLE machines (
  MachineID INT NOT NULL AUTO_INCREMENT,
  GameID INT DEFAULT NULL,
  GameCategory INT DEFAULT NULL,
  Status VARCHAR(25) NOT NULL,
  PRIMARY KEY (MachineID),
  KEY GameID (GameID),
  KEY GameCategory (GameCategory),
  CONSTRAINT machines_ibfk_1 FOREIGN KEY (GameID) REFERENCES GAMES (GameID),
  CONSTRAINT machines_ibfk_2 FOREIGN KEY (GameCategory) REFERENCES GAMECATEGORIES (CategoryID)
) ENGINE=InnoDB AUTO_INCREMENT=300 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Creating the CUSTOMERS table
DROP TABLE IF EXISTS CUSTOMERS;
CREATE TABLE CUSTOMERS (
  CustomerID INT NOT NULL AUTO_INCREMENT,
  CustomerName VARCHAR(40) NOT NULL,
  PhoneNumber VARCHAR(11) NOT NULL,
  EmailID VARCHAR(70) NOT NULL,
  MembershipsCount INT DEFAULT '0',
  CreditsRemaining INT DEFAULT '0',
  Username VARCHAR(50) NOT NULL,
  Password VARCHAR(50) NOT NULL,
  tokens_gained INT DEFAULT '0',
  PRIMARY KEY (CustomerID)
  
  
) ENGINE=InnoDB AUTO_INCREMENT=400 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

select * from customers;
select * from redeemablestore;

-- Creating the MEMBERSHIPS table
DROP TABLE IF EXISTS memberships;
CREATE TABLE memberships (
  MembershipID INT NOT NULL AUTO_INCREMENT,
  MembershipPlan VARCHAR(25) NOT NULL,
  CustomerID INT,
  CardNumber VARCHAR(20) NOT NULL,
  Credits INT NOT NULL,
  StartDate DATE NOT NULL,
  EXPIRY_DATE DATE DEFAULT NULL,
  price INT DEFAULT NULL,
  PRIMARY KEY (MembershipID),
  CONSTRAINT membership_ibfk_1 FOREIGN KEY (CustomerID) REFERENCES CUSTOMERS (CustomerID)
) ENGINE=InnoDB AUTO_INCREMENT=500 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Creating the noofpeoplevisited table
DROP TABLE IF EXISTS noofpeoplevisited;
CREATE TABLE noofpeoplevisited (
  GamePlayID INT NOT NULL AUTO_INCREMENT,
  CustomerID INT DEFAULT NULL,
  PlayDate DATE DEFAULT NULL,
  CreditsSpent INT DEFAULT NULL,
  PRIMARY KEY (GamePlayID),
  CONSTRAINT CustomerID_ibfk FOREIGN KEY (CustomerID) REFERENCES CUSTOMERS (CustomerID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Creating the STAFF table
DROP TABLE IF EXISTS staff;
CREATE TABLE staff (
  StaffID INT NOT NULL AUTO_INCREMENT,
  StaffName VARCHAR(255) NOT NULL,
  Department VARCHAR(255) NOT NULL,
  StaffPhoneNumber VARCHAR(15) NOT NULL,
  Shifthours VARCHAR(25), 
  staff_username VARCHAR(6) DEFAULT NULL,
  staff_password VARCHAR(20) DEFAULT NULL,
  PRIMARY KEY (StaffID)
) ENGINE=InnoDB AUTO_INCREMENT=600 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Inserting data into the STAFF table
INSERT INTO staff (StaffName, Department, StaffPhoneNumber, Shifthours, staff_username, staff_password) VALUES
('John Doe', 'Sales', '1234567890', '9 AM - 5 PM', 'qwe', 'qwe'),
('Jane Smith', 'Customer Service', '9876543210', '1 PM - 9 PM', 'asd', 'asd'),
('Bob Johnson', 'Technical Support', '8765432109', '10 AM - 6 PM', 'BJ3', 'pass789'),
('Alice Williams', 'Marketing', '7654321098', '8 AM - 4 PM', 'AW4', 'pass012'),
('Charlie Brown', 'HR', '6543210987', '12 PM - 8 PM', 'CB5', 'pass345'),
('Emma Davis', 'Finance', '5432109876', '9 AM - 5 PM', 'ED6', 'pass678'),
('Michael Wilson', 'IT', '4321098765', '11 AM - 7 PM', 'MW7', 'pass901'),
('Olivia Miller', 'Legal', '3210987654', '8 AM - 4 PM', 'OM8', 'pass234'),
('David Jones', 'Operations', '2109876543', '10 AM - 6 PM', 'DJ9', 'pass567'),
('Sophia Johnson', 'Customer Service', '1098765432', '1 PM - 9 PM', 'S10', 'pass890'),
('Ethan Davis', 'Sales', '9876543210', '9 AM - 5 PM', 'ED11', 'pass123'),
('Ava Smith', 'Technical Support', '8765432109', '10 AM - 6 PM', 'AS12', 'pass456'),
('Mia Brown', 'Marketing', '7654321098', '8 AM - 4 PM', 'MB13', 'pass789'),
('Liam Wilson', 'HR', '6543210987', '12 PM - 8 PM', 'LW14', 'pass012'),
('Isabella Miller', 'Finance', '5432109876', '9 AM - 5 PM', 'IM15', 'pass345'),
('Noah Jones', 'IT', '4321098765', '11 AM - 7 PM', 'NJ16', 'pass678'),
('Sophia Davis', 'Legal', '3210987654', '8 AM - 4 PM', 'SD17', 'pass901'),
('Logan Williams', 'Operations', '2109876543', '10 AM - 6 PM', 'LW18', 'pass234'),
('Olivia Johnson', 'Customer Service', '1098765432', '1 PM - 9 PM', 'OJ19', 'pass567'),
('Lucas Brown', 'Sales', '9876543210', '9 AM - 5 PM', 'LB20', 'pass890');


-- Creating the REDEEMABLESTORE table
DROP TABLE IF EXISTS REDEEMABLESTORE;
CREATE TABLE REDEEMABLESTORE (
  ProductID INT NOT NULL AUTO_INCREMENT,
  ProductName VARCHAR(255) NOT NULL,
  tokens_required DECIMAL(10,2) NOT NULL,
  Availability INT NOT NULL,
  PRIMARY KEY (ProductID)
) ENGINE=InnoDB AUTO_INCREMENT=700 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Creating the customertokenlog table
DROP TABLE IF EXISTS customertokenlog;
CREATE TABLE customertokenlog (
  LogID INT NOT NULL AUTO_INCREMENT,
  CustomerID INT DEFAULT NULL,
  OldTokens INT DEFAULT NULL,
  NewTokens INT DEFAULT NULL,
  Timestamp TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (LogID)
) ENGINE=InnoDB AUTO_INCREMENT=800 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Creating the machinestatuslog table
DROP TABLE IF EXISTS machinestatuslog;
CREATE TABLE machinestatuslog (
  LogID INT NOT NULL AUTO_INCREMENT,
  MachineID INT DEFAULT NULL,
  OldStatus VARCHAR(20) DEFAULT NULL,
  NewStatus VARCHAR(20) DEFAULT NULL,
  Timestamp TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (LogID)
) ENGINE=InnoDB AUTO_INCREMENT=900 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Creating the GetMachinegames stored procedure
DELIMITER //
CREATE PROCEDURE GetMachinegames()
BEGIN
    SELECT
        m.MachineID,
        m.Status,
        g.GameID,
        g.Name AS GameName,
        g.credits_required
    FROM
        machines m
    LEFT JOIN games g ON m.GameID = g.GameID
    WHERE
        m.Status = 'Stand_by';
END;
//
DELIMITER ;
