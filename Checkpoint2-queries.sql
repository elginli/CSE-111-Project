.headers on 

INSERT INTO Customer (CustomerID, Name, Email, Address)
VALUES
    (11, 'John', 'alice@email.com', '123 Main St, Springfield, CA');

-- Products
INSERT INTO Product (ProductID, Name, Price, Category, StockQuantity)
VALUES
    (11, 'TV', 3200.00, 'Electronics', 20);
-- Orders
INSERT INTO `Order` (OrderID, OrderDate, TotalAmount, ShippingAddress, CustomerID)
VALUES

    (11, '2024-11-8', 3200.00, '707 G St, Merced, CA', 11);

-- Suppliers
INSERT INTO Supplier (SupplierID, Name, ContactInfo, Address)
VALUES

    (11, 'Supplier K', 'contactK@email.com', '505 G St, Merced, CA');

-- Inventory
INSERT INTO Inventory (InventoryID, ProductID, StockQuantity, StaffID)
VALUES
    (11, 11, 70, 2);

-- Shipments
INSERT INTO Shipment (ShipmentID, OrderID, ShipmentDate, Status, SupplierID)
VALUES
    (11, 11, '2024-11-10', 'In Transit', 11);

-- Staff
INSERT INTO Staff (StaffID, Name, Role, Email, Address)
VALUES
    (11, 'Santosh', 'Inventory Manager', 'santosh@email.com', '505 Grand St, Los Angeles, CA');

-- OrderProduct (associating orders and products)
INSERT INTO OrderProduct (OrderID, ProductID, Quantity)
VALUES
    (11, 11, 1);

-- SupplierProduct (associating suppliers and products)
INSERT INTO SupplierProduct (SupplierID, ProductID)
VALUES
    (11, 11);



-- Update

UPDATE Product
SET price = 750
WHERE productID = 11;


UPDATE Product
SET StockQuantity = StockQuantity + 20
WHERE productID = 11;


UPDATE Supplier
SET contact = 'newcontact@example.com'
WHERE supplierID = 1;

UPDATE Customer
SET 'Name' = 'John'
Where CustomerID = 11;



-- Deleting 
Delete  
FROM Customer
WHERE CustomerID = '11';

Delete  
FROM 'Order'
WHERE CustomerID = '11';

DELETE FROM OrderProduct
WHERE OrderProduct.OrderID IN (
    SELECT 'Order'.OrderID
    FROM 'Order'
    JOIN Customer ON 'Order'.CustomerID = Customer.CustomerID
    WHERE Customer.CustomerID = 11
);

Delete  
FROM Product
WHERE ProductID = '11';

Delete  
FROM Shipment
WHERE Shipment.ShipmentID IN (
    SELECT 'Order'.OrderID
    FROM 'Order'
    JOIN Customer ON 'Order'.CustomerID = Customer.CustomerID
    WHERE Customer.CustomerID = 11
);

Delete  
FROM Customer
WHERE CustomerID = '11';

-- Select statements

SELECT * FROM Customer;
SELECT * FROM Inventory;
SELECT * FROM 'Order';
SELECT * FROM OrderProduct;
SELECT * FROM PRODUCT;
SELECT * FROM Shipment;
SELECT * FROM Staff;
SELECT * FROM Supplier;
SELECT * FROM SupplierProduct;

-- Find total stock value

SELECT SUM(price * StockQuantity) AS TotalStockValue
FROM Product;


-- finding stock that are less than 10
SELECT * FROM Product
WHERE StockQuantity < 10;


-- Finding product by price that is higher than 500
SELECT Product.name 

FROM Product

WHERE Price > 500;


-- Order by price from Cheapest 
SELECT *

FROM Product

ORDER BY Product.price ASC;

-- Order by price from most expensive
SELECT *

FROM Product

ORDER BY Product.price DESC;

-- Finding product by category
SELECT *

FROM Product

WHERE Product.Category = "Electronics"

ORDER BY Product.ProductID;

SELECT *

FROM Product

WHERE Product.Category = "Accessories"

ORDER BY Product.ProductID;

-- finding orders that are after oct 1 2024
SELECT * FROM 'Order'
WHERE OrderDate >= '2024-10-01'
ORDER BY OrderDate DESC;




-- Everyones Order

SELECT Customer.Name, Product.Name AS Item, 'Order'.OrderID AS Order_id

From 'Order', Product

Join OrderProduct ON OrderProduct.OrderID = 'Order'.OrderID AND OrderProduct.ProductID = Product.ProductID

Join Customer ON 'Order'.CustomerID = Customer.CustomerID

Group by 'Order'.OrderID;


-- Everyones Order with Shipment status

SELECT Customer.Name, Product.Name AS Item, 'Order'.OrderID AS Order_id, Shipment.ShipmentDate AS Shipment_date, Shipment.Status

From 'Order', Product

Join OrderProduct ON OrderProduct.OrderID = 'Order'.OrderID AND OrderProduct.ProductID = Product.ProductID

Join Customer ON 'Order'.CustomerID = Customer.CustomerID

Join Shipment ON 'Order'.OrderID = Shipment.OrderID

Group by 'Order'.OrderID;


-- Single person Order search
SELECT Customer.Name, Product.Name AS Item, 'Order'.OrderID AS Order_id, Shipment.ShipmentDate AS Shipment_date, Shipment.Status

From 'Order', Product

Join OrderProduct ON OrderProduct.OrderID = 'Order'.OrderID AND OrderProduct.ProductID = Product.ProductID

Join Customer ON 'Order'.CustomerID = Customer.CustomerID

Join Shipment ON 'Order'.OrderID = Shipment.OrderID

Where 'Order'.OrderID = '5'
Group by 'Order'.OrderID;

