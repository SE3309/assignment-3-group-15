-- Delete statements to delete existing records so I can keep running the statements to debug
DELETE FROM Listing;
DELETE FROM User;
DELETE FROM Address;
DELETE FROM Category;
ALTER TABLE Category AUTO_INCREMENT = 1;
ALTER TABLE Listing AUTO_INCREMENT = 1;

-- Other simple inserts for the foreign key constraints
INSERT INTO Address VALUES (1, '1915 Western Avenue', 'London', 'Ontario', 'N5X8N7', 'Canada');
INSERT INTO Address VALUES (2, '18 North Road', 'New York', 'New York State', '10009', 'United States of America');
INSERT INTO Category (name) VALUES('Electronics');
INSERT INTO Category (name) VALUES ('Sports');
INSERT INTO User VALUES ('hkim946', 'hkim946', '1234password', 'Seller', '2263428593', 'harrykim@gmail.com');
INSERT INTO User VALUES ('seller123', 'seller123', 'password0000', 'Seller', '4832022423', 'sellingman23@outlook.com');

    
-- First insert statement   
INSERT INTO Listing VALUES
(
	0,
    'hkim946',
    1,
    295.95,
    'Brand new Playstation 5',
    1,
    'ps5_image.jpg'
    );
	
-- Second Insert Statement
INSERT INTO Listing (
    seller,
    categoryID,
    price,
    description,
    addressID,
    images
) VALUES (
        'hkim946',
        (SELECT categoryID FROM Category WHERE name = 'Electronics' LIMIT 1),
        599.99,
        'Used, almost new iPhone 15',
        (SELECT AddressID FROM Address WHERE streetAddress = '1915 Western Avenue'LIMIT 1),
        'phone_pic.jpg'
        );

-- Third insert statement
INSERT INTO Listing (seller, categoryID, price, description, addressID, images)
SELECT 'seller123', 2, 249.99, 'Used Bicycle in excellent condition', addressID, 'bicycle_image.jpg'
FROM Category, Address
WHERE Category.name = 'Sports' AND Address.city = 'New York' LIMIT 1;


-- Select statement for Listing table
SELECT * FROM Listing
      

 
        
