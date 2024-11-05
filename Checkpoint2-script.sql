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

-- Creating tables for each entity

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
    StaffID INT, 
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

-- Inserting data to tables
-- Customers
INSERT INTO Customer (CustomerID, Name, Email, Address)
VALUES
    (1, 'Alice', 'alice@email.com', '123 Main St, Springfield, CA'),
    (2, 'Bob', 'bob@email.com', '456 Elm St, Riverside, CA'),
    (3, 'Charlie', 'charlie@email.com', '789 Pine St, Bakersfield, CA'),
    (4, 'David', 'david@email.com', '101 Maple St, Anaheim, CA'),
    (5, 'Eve', 'eve@email.com', '202 Oak St, Long Beach, CA'),
    (6, 'Frank', 'frank@email.com', '303 Cedar St, Fresno, CA'),
    (7, 'Grace', 'grace@email.com', '404 Walnut St, Irvine, CA'),
    (8, 'Hannah', 'hannah@email.com', '505 Birch St, Sacramento, CA'),
    (9, 'Ivy', 'ivy@email.com', '606 Ash St, San Diego, CA'),
    (10, 'Jack', 'jack@email.com', '707 Cherry St, San Francisco, CA');

-- Products
INSERT INTO Product (ProductID, Name, Price, Category, StockQuantity)
VALUES
    (1, 'Laptop', 1200.00, 'Electronics', 50),
    (2, 'Smartphone', 800.00, 'Electronics', 200),
    (3, 'Tablet', 600.00, 'Electronics', 150),
    (4, 'Headphones', 100.00, 'Accessories', 300),
    (5, 'Camera', 500.00, 'Electronics', 75),
    (6, 'Monitor', 300.00, 'Electronics', 100),
    (7, 'Keyboard', 50.00, 'Accessories', 250),
    (8, 'Mouse', 30.00, 'Accessories', 400),
    (9, 'Charger', 20.00, 'Accessories', 500),
    (10, 'Printer', 200.00, 'Electronics', 60);

-- Orders
INSERT INTO `Order` (OrderID, OrderDate, TotalAmount, ShippingAddress, CustomerID)
VALUES
    (1, '2024-10-01', 2000.00, '123 Main St, Springfield, CA', 1),
    (2, '2024-10-05', 800.00, '456 Elm St, Riverside, CA', 2),
    (3, '2024-10-07', 600.00, '789 Pine St, Bakersfield, CA', 3),
    (4, '2024-10-10', 150.00, '101 Maple St, Anaheim, CA', 4),
    (5, '2024-10-12', 500.00, '202 Oak St, Long Beach, CA', 5),
    (6, '2024-10-15', 300.00, '303 Cedar St, Fresno, CA', 6),
    (7, '2024-10-18', 250.00, '404 Walnut St, Irvine, CA', 7),
    (8, '2024-10-20', 100.00, '505 Birch St, Sacramento, CA', 8),
    (9, '2024-10-25', 200.00, '606 Ash St, San Diego, CA', 9),
    (10, '2024-10-28', 1200.00, '707 Cherry St, San Francisco, CA', 10);

-- Suppliers
INSERT INTO Supplier (SupplierID, Name, ContactInfo, Address)
VALUES
    (1, 'Supplier A', 'contactA@email.com', '789 Maple Ave, Los Angeles, CA'),
    (2, 'Supplier B', 'contactB@email.com', '101 Oak St, Palo Alto, CA'),
    (3, 'Supplier C', 'contactC@email.com', '123 Cedar St, Berkeley, CA'),
    (4, 'Supplier D', 'contactD@email.com', '456 Pine St, Glendale, CA'),
    (5, 'Supplier E', 'contactE@email.com', '789 Birch St, Irvine, CA'),
    (6, 'Supplier F', 'contactF@email.com', '101 Walnut St, Santa Clara, CA'),
    (7, 'Supplier G', 'contactG@email.com', '202 Cherry St, Sunnyvale, CA'),
    (8, 'Supplier H', 'contactH@email.com', '303 Oak St, Fremont, CA'),
    (9, 'Supplier I', 'contactI@email.com', '404 Maple Ave, Oakland, CA'),
    (10, 'Supplier J', 'contactJ@email.com', '505 Elm St, Cupertino, CA');

-- Inventory
INSERT INTO Inventory (InventoryID, ProductID, StockQuantity, StaffID)
VALUES
    (1, 1, 50, 1),
    (2, 2, 200, 2),
    (3, 3, 150, 1),
    (4, 4, 300, 2),
    (5, 5, 75, 1),
    (6, 6, 100, 2),
    (7, 7, 250, 1),
    (8, 8, 400, 2),
    (9, 9, 500, 1),
    (10, 10, 60, 2);

-- Shipments
INSERT INTO Shipment (ShipmentID, OrderID, ShipmentDate, Status, SupplierID)
VALUES
    (1, 1, '2024-10-02', 'Shipped', 1),
    (2, 2, '2024-10-06', 'In Transit', 2),
    (3, 3, '2024-10-08', 'Delivered', 3),
    (4, 4, '2024-10-11', 'Pending', 4),
    (5, 5, '2024-10-13', 'Shipped', 5),
    (6, 6, '2024-10-16', 'Cancelled', 6),
    (7, 7, '2024-10-19', 'Delivered', 7),
    (8, 8, '2024-10-21', 'Pending', 8),
    (9, 9, '2024-10-26', 'Shipped', 9),
    (10, 10, '2024-10-29', 'In Transit', 10);

-- Staff
INSERT INTO Staff (StaffID, Name, Role, Email, Address)
VALUES
    (1, 'John', 'Inventory Manager', 'john@email.com', '321 Pine St, Palo Alto, CA'),
    (2, 'Sarah', 'Inventory Manager', 'sarah@email.com', '654 Cedar St, San Jose, CA'),
    (3, 'Alex', 'Sales Associate', 'alex@email.com', '123 Oak St, Santa Cruz, CA'),
    (4, 'Emily', 'Sales Associate', 'emily@email.com', '456 Birch St, San Mateo, CA'),
    (5, 'Michael', 'Inventory Assistant', 'michael@email.com', '789 Maple St, Redwood City, CA'),
    (6, 'Rachel', 'Inventory Assistant', 'rachel@email.com', '101 Walnut St, Mountain View, CA'),
    (7, 'Tom', 'Inventory Manager', 'tom@email.com', '202 Cedar St, Los Gatos, CA'),
    (8, 'Linda', 'Sales Associate', 'linda@email.com', '303 Cherry St, San Bruno, CA'),
    (9, 'Henry', 'Sales Associate', 'henry@email.com', '404 Elm St, Milpitas, CA'),
    (10, 'Anna', 'Inventory Manager', 'anna@email.com', '505 Pine St, Gilroy, CA');

-- OrderProduct (associating orders and products)
INSERT INTO OrderProduct (OrderID, ProductID, Quantity)
VALUES
    (1, 1, 1),
    (2, 2, 1),
    (3, 3, 2),
    (4, 4, 3),
    (5, 5, 1),
    (6, 6, 1),
    (7, 7, 2),
    (8, 8, 3),
    (9, 9, 1),
    (10, 10, 1);

-- SupplierProduct (associating suppliers and products)
INSERT INTO SupplierProduct (SupplierID, ProductID)
VALUES
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10);


--SQL statements


