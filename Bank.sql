CREATE DATABASE  IF NOT EXISTS `bank` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `bank`;
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: bank
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `accounts`
--

DROP TABLE IF EXISTS `accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts` (
  `AccountID` int NOT NULL AUTO_INCREMENT,
  `AccountNumber` varchar(8) NOT NULL,
  `AccountHolderID` int NOT NULL,
  `AccountType` enum('Savings','Current','Salary','Recurring Deposit','Fixed Deposit') NOT NULL,
  `AccountBalance` decimal(15,2) NOT NULL DEFAULT '0.00',
  `AccountOpened` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `AccountStatus` enum('Active','Inactive','Closed','Frozen') NOT NULL DEFAULT 'Active',
  `AccountSecondaryHolderID` int DEFAULT NULL,
  `AccountPassword` varchar(15) NOT NULL,
  PRIMARY KEY (`AccountID`),
  UNIQUE KEY `AccountNumber` (`AccountNumber`),
  KEY `Accountholder` (`AccountHolderID`),
  KEY `AccountSecondaryHolderID` (`AccountSecondaryHolderID`),
  CONSTRAINT `accounts_ibfk_1` FOREIGN KEY (`AccountHolderID`) REFERENCES `customers` (`CustomerID`) ON DELETE CASCADE,
  CONSTRAINT `accounts_ibfk_2` FOREIGN KEY (`AccountSecondaryHolderID`) REFERENCES `customers` (`CustomerID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts`
--

LOCK TABLES `accounts` WRITE;
/*!40000 ALTER TABLE `accounts` DISABLE KEYS */;
INSERT INTO `accounts` VALUES (15,'00000001',1,'Current',10000000.00,'2025-01-02 18:56:15','Active',NULL,'vault123');
/*!40000 ALTER TABLE `accounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `branches`
--

DROP TABLE IF EXISTS `branches`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `branches` (
  `BranchId` int NOT NULL AUTO_INCREMENT,
  `BranchName` varchar(50) NOT NULL,
  `BranchAddress` varchar(300) NOT NULL,
  `BranchContactNumber` varchar(15) NOT NULL,
  `BranchEmployeeCount` int NOT NULL,
  PRIMARY KEY (`BranchId`),
  UNIQUE KEY `BranchName` (`BranchName`),
  UNIQUE KEY `BranchAddress` (`BranchAddress`),
  UNIQUE KEY `BranchContactNumber` (`BranchContactNumber`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `branches`
--

LOCK TABLES `branches` WRITE;
/*!40000 ALTER TABLE `branches` DISABLE KEYS */;
INSERT INTO `branches` VALUES (1,'Headquarters','Gringotts, Diagon Alley, London, England','123-MAGIC-789',1);
/*!40000 ALTER TABLE `branches` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cards`
--

DROP TABLE IF EXISTS `cards`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cards` (
  `CardID` int NOT NULL AUTO_INCREMENT,
  `CardNumber` varchar(16) DEFAULT NULL,
  `CardHolderAccountID` int NOT NULL,
  `CardIssuer` enum('Visa','Mastercard','Rupay','American Express') NOT NULL,
  `CardType` enum('Debit','Credit','Prepaid','ATM') NOT NULL,
  `CardHolderFirstName` varchar(50) NOT NULL,
  `CardHolderLastName` varchar(50) NOT NULL,
  `CardIssueDate` datetime DEFAULT CURRENT_TIMESTAMP,
  `CardExpiaryDate` date DEFAULT NULL,
  `Card_CVV_Code` varchar(4) DEFAULT NULL,
  `CardStatus` enum('Active','Blocked','Missing','Pending') NOT NULL DEFAULT 'Active',
  `CardAnnualFees` int NOT NULL DEFAULT '200',
  `CardPrePaidAmt` decimal(12,5) DEFAULT NULL,
  PRIMARY KEY (`CardID`),
  UNIQUE KEY `CardNumber` (`CardNumber`),
  UNIQUE KEY `CardNumber_2` (`CardNumber`),
  KEY `CardHolderAccountID` (`CardHolderAccountID`),
  CONSTRAINT `cards_ibfk_1` FOREIGN KEY (`CardHolderAccountID`) REFERENCES `accounts` (`AccountID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cards`
--

LOCK TABLES `cards` WRITE;
/*!40000 ALTER TABLE `cards` DISABLE KEYS */;
/*!40000 ALTER TABLE `cards` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers` (
  `CustomerID` int NOT NULL AUTO_INCREMENT,
  `Firstname` varchar(50) NOT NULL,
  `Lastname` varchar(50) NOT NULL,
  `DateOfBirth` date NOT NULL,
  `ContactNumber` varchar(15) NOT NULL,
  `EmailID` varchar(256) NOT NULL,
  `PermanentResidence` varchar(300) NOT NULL,
  `RegisteredIDType` enum('AadharCard','Passport','PANCard','Driving License','Other') NOT NULL,
  `IDNumber` varchar(50) NOT NULL,
  `IDExpiryDate` date NOT NULL,
  `AccountStatus` enum('Active','Inactive','Suspended') DEFAULT 'Active',
  `CreatedAt` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `UpdatedAt` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `CustomerPassword` varchar(15) NOT NULL,
  PRIMARY KEY (`CustomerID`),
  UNIQUE KEY `IDNumber` (`IDNumber`),
  UNIQUE KEY `EmailID` (`EmailID`),
  UNIQUE KEY `ContactNumber` (`ContactNumber`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES (1,'Admin','Root','1800-01-01','123-MAGIC-789','admin@root.com','Gringotts, Diagon Alley, London, England','Other','000000000','2100-12-31','Active','2025-01-02 18:54:53','2025-01-02 18:54:53','root');
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employees`
--

DROP TABLE IF EXISTS `employees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employees` (
  `EmployeeID` int NOT NULL AUTO_INCREMENT,
  `EmployeeFirstName` varchar(50) NOT NULL,
  `EmployeeLastName` varchar(50) NOT NULL,
  `EmployeeDOB` date NOT NULL,
  `EmployeeContactNumber` varchar(15) NOT NULL,
  `EmployeePersonalEmailID` varchar(256) NOT NULL,
  `EmployeeCompanyAssignedEmailID` varchar(256) NOT NULL,
  `EmployeeResidenceAddress` varchar(300) NOT NULL,
  `EmployeeBranchID` int NOT NULL,
  `EmployeePositionShortCode` int NOT NULL,
  `EmployeePayRaisePercentage` decimal(5,2) DEFAULT NULL,
  `EmployeeRegisteredIDType` enum('AadhaarCard','PANCard','DrivingLicense','Other') NOT NULL,
  `EmployeeIDNumber` varchar(50) NOT NULL,
  `EmployeeIDExpiryDate` date NOT NULL,
  `EmployeeJoinDate` datetime DEFAULT CURRENT_TIMESTAMP,
  `EmployeeGender` enum('Male','Female','Other') NOT NULL,
  `EmployeeMaritalStatus` enum('Single','Married','Divorced','Widowed') NOT NULL,
  `EmployeeEmploymentStatus` enum('Employed','On Leave','Resigned','Fired') NOT NULL DEFAULT 'Employed',
  `EmployeeBankAccountID` int NOT NULL,
  `EmployeePrivilege` enum('Top_Level_Admin','Admin','None') NOT NULL,
  `EmployeePassword` varchar(15) NOT NULL,
  PRIMARY KEY (`EmployeeID`),
  UNIQUE KEY `EmployeeIDNumber` (`EmployeeIDNumber`),
  KEY `EmployeeBranchID` (`EmployeeBranchID`),
  KEY `EmployeePositionShortCode` (`EmployeePositionShortCode`),
  KEY `EmployeeBankAccountID` (`EmployeeBankAccountID`),
  CONSTRAINT `employees_ibfk_1` FOREIGN KEY (`EmployeeBranchID`) REFERENCES `branches` (`BranchId`),
  CONSTRAINT `employees_ibfk_2` FOREIGN KEY (`EmployeePositionShortCode`) REFERENCES `positionshortcodes` (`PositionID`),
  CONSTRAINT `employees_ibfk_3` FOREIGN KEY (`EmployeeBankAccountID`) REFERENCES `accounts` (`AccountID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employees`
--

LOCK TABLES `employees` WRITE;
/*!40000 ALTER TABLE `employees` DISABLE KEYS */;
INSERT INTO `employees` VALUES (1,'Admin','root','1800-01-01','123-MAGIC-789','admin@root.com','admin@root.com','Gringotts, Diagon Alley, London, England',1,1,0.00,'Other','000000000','2100-12-31','2025-01-03 00:27:41','Other','Single','Employed',1,'Top_Level_Admin','root');
/*!40000 ALTER TABLE `employees` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `loans`
--

DROP TABLE IF EXISTS `loans`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `loans` (
  `LoanID` int NOT NULL AUTO_INCREMENT,
  `CustomerID` int NOT NULL,
  `LoanType` enum('Home Loan','Gold Loan','Vehicle Loan','Mortgage Loan','Personal Loan','Education Loan') NOT NULL,
  `LoanAmmount` decimal(12,2) NOT NULL,
  `LoanInterestRate` decimal(5,2) NOT NULL DEFAULT '8.00',
  `LoanStartDate` datetime DEFAULT CURRENT_TIMESTAMP,
  `LoanMaturityDate` date DEFAULT NULL,
  `LoanStatus` enum('Approved','Rejected','Pending','Paid','Defaulted') NOT NULL DEFAULT 'Pending',
  `LoanUpdateDate` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `LoanAmmountDue` decimal(12,2) NOT NULL DEFAULT (`LoanAmmount`),
  PRIMARY KEY (`LoanID`),
  KEY `CustomerID` (`CustomerID`),
  CONSTRAINT `loans_ibfk_1` FOREIGN KEY (`CustomerID`) REFERENCES `customers` (`CustomerID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `loans`
--

LOCK TABLES `loans` WRITE;
/*!40000 ALTER TABLE `loans` DISABLE KEYS */;
/*!40000 ALTER TABLE `loans` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `logs`
--

DROP TABLE IF EXISTS `logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `logs` (
  `EmployeeID` int DEFAULT NULL,
  `Event` text NOT NULL,
  `Occurred_At` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `Status` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`Occurred_At`),
  KEY `FK_Logs_Employees` (`EmployeeID`),
  CONSTRAINT `FK_Logs_Employees` FOREIGN KEY (`EmployeeID`) REFERENCES `employees` (`EmployeeID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logs`
--

LOCK TABLES `logs` WRITE;
/*!40000 ALTER TABLE `logs` DISABLE KEYS */;
/*!40000 ALTER TABLE `logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `positionshortcodes`
--

DROP TABLE IF EXISTS `positionshortcodes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `positionshortcodes` (
  `PositionID` int NOT NULL AUTO_INCREMENT,
  `PositionFullName` varchar(50) NOT NULL,
  `PositionDefaultPay` int NOT NULL,
  PRIMARY KEY (`PositionID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `positionshortcodes`
--

LOCK TABLES `positionshortcodes` WRITE;
/*!40000 ALTER TABLE `positionshortcodes` DISABLE KEYS */;
INSERT INTO `positionshortcodes` VALUES (1,'Default Admin',-1);
/*!40000 ALTER TABLE `positionshortcodes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transactionlogs`
--

DROP TABLE IF EXISTS `transactionlogs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transactionlogs` (
  `TransactionID` int NOT NULL AUTO_INCREMENT,
  `DebitAccountID` int NOT NULL,
  `CreditAccountID` int NOT NULL,
  `TransactionType` enum('Deposit','Withdrawal','Transfer') NOT NULL,
  `TransactionAmount` decimal(10,2) NOT NULL,
  `TransactionDate` datetime DEFAULT CURRENT_TIMESTAMP,
  `TransactionDescription` text,
  `TransactionMedium` enum('Cash','Cheque','Netbanking','Other') NOT NULL,
  PRIMARY KEY (`TransactionID`),
  KEY `DebitUserID` (`DebitAccountID`),
  KEY `CreditUserID` (`CreditAccountID`),
  CONSTRAINT `transactionlogs_ibfk_1` FOREIGN KEY (`DebitAccountID`) REFERENCES `accounts` (`AccountID`),
  CONSTRAINT `transactionlogs_ibfk_2` FOREIGN KEY (`CreditAccountID`) REFERENCES `accounts` (`AccountID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transactionlogs`
--

LOCK TABLES `transactionlogs` WRITE;
/*!40000 ALTER TABLE `transactionlogs` DISABLE KEYS */;
/*!40000 ALTER TABLE `transactionlogs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'bank'
--

--
-- Dumping routines for database 'bank'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
