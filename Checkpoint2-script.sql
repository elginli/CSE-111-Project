-- Dropping tables if they already exist to avoid errors
DROP TABLE IF EXISTS Shipment;
DROP TABLE IF EXISTS Inventory;
DROP TABLE IF EXISTS OrderProduct;
DROP TABLE IF EXISTS SupplierProduct;
DROP TABLE IF EXISTS `Order`;
DROP TABLE IF EXISTS Product;
DROP TABLE IF EXISTS Customer;
DROP TABLE IF EXISTS Supplier;
DROP TABLE IF EXISTS Staff;

-- Creating tables for each entity with attributes

CREATE TABLE Staff (
    StaffID INT PRIMARY KEY,
    Name VARCHAR(255),
    Role VARCHAR(10),
    Email VARCHAR(255),
    Address VARCHAR(255)
);

CREATE TABLE Customer (
    CustomerID INT PRIMARY KEY,
    Name VARCHAR(255),
    Email VARCHAR(255),
    Address VARCHAR(255)
);

CREATE TABLE Product (
    ProductID INT PRIMARY KEY,
    Name VARCHAR(255),
    Price DECIMAL(10, 2),
    Category VARCHAR(255),
    StockQuantity INT
);

CREATE TABLE `Order` (
    OrderID INT PRIMARY KEY,
    OrderDate DATE,
    TotalAmount DECIMAL(10, 2),
    ShippingAddress VARCHAR(255),
    CustomerID INT,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
);

CREATE TABLE Supplier (
    SupplierID INT PRIMARY KEY,
    Name VARCHAR(255),
    ContactInfo VARCHAR(255),
    Address VARCHAR(255)
);

CREATE TABLE Inventory (
    InventoryID INT PRIMARY KEY,
    ProductID INT UNIQUE,
    StockQuantity INT,
    StaffID INT,  -- Include StaffID here
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID),
    FOREIGN KEY (StaffID) REFERENCES Staff(StaffID)
);

CREATE TABLE Shipment (
    ShipmentID INT PRIMARY KEY,
    OrderID INT UNIQUE,
    ShipmentDate DATE,
    Status VARCHAR(255),
    SupplierID INT,
    FOREIGN KEY (OrderID) REFERENCES `Order`(OrderID),
    FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID)
);

-- Associative tables for Many-to-Many relationships

CREATE TABLE OrderProduct (
    OrderID INT,
    ProductID INT,
    Quantity INT,
    PRIMARY KEY (OrderID, ProductID),
    FOREIGN KEY (OrderID) REFERENCES `Order`(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);

CREATE TABLE SupplierProduct (
    SupplierID INT,
    ProductID INT,
    PRIMARY KEY (SupplierID, ProductID),
    FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID),
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);

-- Inserting example data into tables

-- Customers
INSERT INTO Customer (CustomerID, Name, Email, Address)
VALUES
    (1, 'Alice', 'alice@example.com', '123 Main St'),
    (2, 'Bob', 'bob@example.com', '456 Elm St');

-- Products
INSERT INTO Product (ProductID, Name, Price, Category, StockQuantity)
VALUES
    (1, 'Laptop', 1200.00, 'Electronics', 50),
    (2, 'Smartphone', 800.00, 'Electronics', 200);

-- Orders
INSERT INTO `Order` (OrderID, OrderDate, TotalAmount, ShippingAddress, CustomerID)
VALUES
    (1, '2024-10-01', 2000.00, '123 Main St', 1),
    (2, '2024-10-05', 800.00, '456 Elm St', 2);

-- Suppliers
INSERT INTO Supplier (SupplierID, Name, ContactInfo, Address)
VALUES
    (1, 'Supplier A', 'contactA@example.com', '789 Maple Ave'),
    (2, 'Supplier B', 'contactB@example.com', '101 Oak St');

-- Inventory
INSERT INTO Inventory (InventoryID, ProductID, StockQuantity, StaffID)
VALUES
    (1, 1, 50, 1),
    (2, 2, 200, 2);

-- Shipments
INSERT INTO Shipment (ShipmentID, OrderID, ShipmentDate, Status, SupplierID)
VALUES
    (1, 1, '2024-10-02', 'Shipped', 1),
    (2, 2, '2024-10-06', 'In Transit', 2);

-- Staff
INSERT INTO Staff (StaffID, Name, Role, Email, Address)
VALUES
    (1, 'John', 'Inventory Manager', 'john@example.com', '321 Pine St'),
    (2, 'Sarah', 'Inventory Manager', 'sarah@example.com', '654 Cedar St');

-- OrderProduct (associating orders and products)
INSERT INTO OrderProduct (OrderID, ProductID, Quantity)
VALUES
    (1, 1, 1),
    (2, 2, 1);

-- SupplierProduct (associating suppliers and products)
INSERT INTO SupplierProduct (SupplierID, ProductID)
VALUES
    (1, 1),
    (2, 2);
