-- Delete statements to delete existing records so I can keep running the statements to debug
DELETE FROM Listing WHERE listingID IN (123, 2);
DELETE FROM Address WHERE addressID IN (5, 8);
DELETE FROM Category WHERE categoryID IN (2, 4);
DELETE FROM User WHERE displayName = 'hkim946';
DELETE FROM User WHERE userID = 8;




-- First insert statement
INSERT INTO User VALUES
(
	1,
    'hkim946',
    '1234password',
    'Seller',
    '2263428593',
    'harrykim@gmail.com'
    );

-- Second Insert Statement
-- Other simple inserts for the foreign key constraints
INSERT INTO Category VALUES
(
	2,
    'Electronics'
);
INSERT INTO Address VALUES (5, '1915 Western Avenue', 'London', 'Ontario', 'N5X8N7', 'Canada');
INSERT INTO Listing (
	listingID,
    seller,
    categoryID,
    price,
    description,
    addressID,
    images
) VALUES (
		123,
        1,
        (SELECT categoryID FROM Category WHERE name = 'Electronics'),
        299.99,
        'Used, almost new iPhone 15',
        (SELECT AddressID FROM Address WHERE streetAddress = '1915 Western Avenue'),
        'phonepic.jpg'
        );

-- Third insert statement
-- Simple insert statements for foreign key constraints
INSERT INTO Address VALUES (8, '18 North Road', 'New York', 'New York State', '10009', 'United States of America');
INSERT INTO Category VALUES (4, 'Sports');
INSERT INTO User VALUES (8, 'seller123', 'password0000', 'Seller', '4832022423', 'sellingman23@outlook.com');
INSERT INTO Listing (listingID, seller, categoryID, price, description, addressID, images)
SELECT 2, 8, 4, 249.99, 'Used Bicycle in excellent condition', addressID, 'bicycle_image.jpg'
FROM Category, Address
WHERE Category.name = 'Sports' AND Address.city = 'New York' LIMIT 1;

-- Select statement for Listing table
SELECT *
FROM Listing
WHERE listingID IS NOT NULL;          
 
-- Select statement for User table
SELECT * FROM User WHERE userID IS NOT NULL;

 
        
