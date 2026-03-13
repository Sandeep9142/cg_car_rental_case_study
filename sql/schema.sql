-- ============================================================
-- Car Rental Order Processing System - Database Schema
-- Developer 6 - SQL Analytics
-- ============================================================

-- Customers table
CREATE TABLE CUSTOMERS (
    Customer_ID     INT PRIMARY KEY,
    Name            VARCHAR(100) NOT NULL,
    Email           VARCHAR(150) UNIQUE NOT NULL,
    Phone           VARCHAR(20),
    City            VARCHAR(50),
    Join_Date       DATE NOT NULL,
    Loyalty_Tier    VARCHAR(20) DEFAULT 'Bronze'
);

-- Locations table
CREATE TABLE LOCATIONS (
    Location_ID     INT PRIMARY KEY,
    City            VARCHAR(50) NOT NULL,
    Address         VARCHAR(200),
    Zone            VARCHAR(20),
    Is_Airport      BOOLEAN DEFAULT FALSE,
    Contact_Phone   VARCHAR(20)
);

-- Vehicles table
CREATE TABLE VEHICLES (
    Vehicle_ID      VARCHAR(10) PRIMARY KEY,
    Make            VARCHAR(50) NOT NULL,
    Model           VARCHAR(50) NOT NULL,
    Year            INT,
    Category        VARCHAR(30),
    Daily_Rate      DECIMAL(10, 2) NOT NULL,
    Location_ID     INT,
    Status          VARCHAR(20) DEFAULT 'Available',
    Odometer        INT DEFAULT 0,
    FOREIGN KEY (Location_ID) REFERENCES LOCATIONS(Location_ID)
);

-- Reservations table
CREATE TABLE RESERVATIONS (
    Reservation_ID  VARCHAR(20) PRIMARY KEY,
    Customer_ID     INT NOT NULL,
    Vehicle_ID      VARCHAR(10) NOT NULL,
    Location_ID     INT NOT NULL,
    Pickup_TS       DATETIME NOT NULL,
    Return_TS       DATETIME,
    Odo_Start       INT,
    Odo_End         INT,
    Status          VARCHAR(20) DEFAULT 'Active',
    FOREIGN KEY (Customer_ID) REFERENCES CUSTOMERS(Customer_ID),
    FOREIGN KEY (Vehicle_ID) REFERENCES VEHICLES(Vehicle_ID),
    FOREIGN KEY (Location_ID) REFERENCES LOCATIONS(Location_ID)
);

-- Payments table
CREATE TABLE PAYMENTS (
    Payment_ID      INT PRIMARY KEY,
    Reservation_ID  VARCHAR(20) NOT NULL,
    Amount          DECIMAL(10, 2) NOT NULL,
    Payment_Method  VARCHAR(20) NOT NULL,
    Payment_Date    DATETIME NOT NULL,
    Status          VARCHAR(20) DEFAULT 'Completed',
    FOREIGN KEY (Reservation_ID) REFERENCES RESERVATIONS(Reservation_ID)
);

-- Maintenance table
CREATE TABLE MAINTENANCE (
    Maintenance_ID  INT PRIMARY KEY,
    Vehicle_ID      VARCHAR(10) NOT NULL,
    Maintenance_Type VARCHAR(50) NOT NULL,
    Description     VARCHAR(200),
    Cost            DECIMAL(10, 2),
    Start_Date      DATE NOT NULL,
    End_Date        DATE,
    Status          VARCHAR(20) DEFAULT 'Scheduled',
    FOREIGN KEY (Vehicle_ID) REFERENCES VEHICLES(Vehicle_ID)
);
